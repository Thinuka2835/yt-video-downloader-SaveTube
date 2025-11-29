from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import json
from pathlib import Path
import re

app = Flask(__name__, static_folder='.')
CORS(app)

# Create downloads directory
DOWNLOAD_DIR = Path('downloads')
DOWNLOAD_DIR.mkdir(exist_ok=True)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_ydl_opts(base_opts=None):
    """Get yt-dlp options with bot bypass configuration"""
    opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'age_limit': None,
        'extractor_retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    # Check for cookies.txt file
    cookies_file = Path('cookies.txt')
    if cookies_file.exists():
        opts['cookiefile'] = str(cookies_file)
        print(f"✅ Using cookies from: {cookies_file}")
    else:
        print("ℹ️  No cookies.txt found. See YOUTUBE_BOT_FIX.md for help with bot detection")
    
    if base_opts:
        opts.update(base_opts)
    
    return opts

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    """Serve CSS file"""
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    """Get video metadata without downloading"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        ydl_opts = get_ydl_opts({'extract_flat': False})
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get available formats
            video_formats = []
            audio_formats = []
            
            if 'formats' in info:
                for fmt in info['formats']:
                    # Video formats
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        ext = fmt.get('ext', 'mp4')
                        resolution = fmt.get('resolution', 'unknown')
                        if ext not in [f['ext'] for f in video_formats]:
                            video_formats.append({
                                'ext': ext,
                                'resolution': resolution
                            })
                    
                    # Audio formats
                    if fmt.get('vcodec') == 'none' and fmt.get('acodec') != 'none':
                        ext = fmt.get('ext', 'mp3')
                        if ext not in [f['ext'] for f in audio_formats]:
                            audio_formats.append({'ext': ext})
            
            # Default formats if none found
            if not video_formats:
                video_formats = [
                    {'ext': 'mp4', 'resolution': 'best'},
                    {'ext': 'webm', 'resolution': 'best'},
                    {'ext': 'avi', 'resolution': 'best'},
                    {'ext': 'mov', 'resolution': 'best'}
                ]
            
            if not audio_formats:
                audio_formats = [
                    {'ext': 'mp3'},
                    {'ext': 'wav'},
                    {'ext': 'm4a'},
                    {'ext': 'opus'}
                ]
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'video_formats': video_formats,
                'audio_formats': audio_formats,
                'is_playlist': 'entries' in info
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video or audio in specified format"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('type', 'video')  # 'video' or 'audio'
        output_format = data.get('format', 'mp4')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Configure yt-dlp options
        ydl_opts = get_ydl_opts({
            'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
            'quiet': False,
        })
        
        if format_type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': '192',
            }]
        else:
            # Video download
            if output_format == 'mp4':
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif output_format == 'webm':
                ydl_opts['format'] = 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'
            else:
                ydl_opts['format'] = 'best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': output_format,
                }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Find the downloaded file
            title = sanitize_filename(info.get('title', 'video'))
            
            # Check for the file with the correct extension
            possible_files = list(DOWNLOAD_DIR.glob(f"{title}.*"))
            
            if possible_files:
                downloaded_file = possible_files[0]
                return jsonify({
                    'success': True,
                    'filename': downloaded_file.name,
                    'path': str(downloaded_file),
                    'title': info.get('title', 'Unknown')
                })
            else:
                return jsonify({'error': 'File not found after download'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playlist-info', methods=['POST'])
def get_playlist_info():
    """Get playlist metadata"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        ydl_opts = get_ydl_opts({'extract_flat': True})
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' not in info:
                return jsonify({'error': 'Not a playlist URL'}), 400
            
            videos = []
            for entry in info['entries']:
                if entry:
                    videos.append({
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('url', ''),
                        'duration': entry.get('duration', 0)
                    })
            
            return jsonify({
                'title': info.get('title', 'Unknown Playlist'),
                'video_count': len(videos),
                'videos': videos
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-playlist', methods=['POST'])
def download_playlist():
    """Download entire playlist"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('type', 'video')
        output_format = data.get('format', 'mp4')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Create playlist subdirectory
        playlist_dir = DOWNLOAD_DIR / 'playlist_%(playlist_title)s'
        
        ydl_opts = get_ydl_opts({
            'outtmpl': str(playlist_dir / '%(playlist_index)s - %(title)s.%(ext)s'),
            'quiet': False,
        })
        
        if format_type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': '192',
            }]
        else:
            if output_format == 'mp4':
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif output_format == 'webm':
                ydl_opts['format'] = 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'
            else:
                ydl_opts['format'] = 'best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': output_format,
                }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            video_count = len(info.get('entries', []))
            
            return jsonify({
                'success': True,
                'video_count': video_count,
                'playlist_title': info.get('title', 'Unknown Playlist')
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-file/<path:filename>')
def download_file(filename):
    """Serve downloaded file"""
    try:
        return send_file(DOWNLOAD_DIR / filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    print("🚀 SaveTube Server Starting...")
    print("📁 Downloads will be saved to:", DOWNLOAD_DIR.absolute())
    print("🌐 Server running at: http://localhost:5000")
    print("\n⚠️  Make sure FFmpeg is installed for format conversion!")
    app.run(debug=True, port=5000, host='0.0.0.0')

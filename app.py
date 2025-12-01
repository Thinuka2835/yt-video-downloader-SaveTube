from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
from yt_dlp.utils import DownloadError
import os
import json
from pathlib import Path
import re
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__, static_folder='.')
CORS(app)

# Default download directory
# Default download directory (removed default fallback)
# DOWNLOAD_DIR = Path.home() / "Downloads"
# DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)



# Global dictionary to store download progress
download_progress = {}

def progress_hook(d):
    """Hook to track download progress"""
    if d['status'] == 'downloading':
        download_id = d.get('info_dict', {}).get('download_id')
        if download_id:
            try:
                p = d.get('_percent_str', '0%').replace('%', '')
                download_progress[download_id] = {
                    'status': 'downloading',
                    'percent': float(p),
                    'speed': d.get('_speed_str', 'N/A'),
                    'eta': d.get('_eta_str', 'N/A'),
                    'filename': d.get('filename', 'Unknown')
                }
            except Exception:
                pass
    elif d['status'] == 'finished':
        download_id = d.get('info_dict', {}).get('download_id')
        if download_id:
            download_progress[download_id] = {
                'status': 'finished',
                'percent': 100,
                'filename': d.get('filename', 'Unknown')
            }

import subprocess

def select_download_folder():
    """Open a native folder selection dialog using a separate process"""
    try:
        # Run the dialog.py script and capture output
        result = subprocess.check_output(['python', 'dialog.py'], text=True).strip()
        return result if result else None
    except Exception as e:
        print(f"Error selecting folder: {e}")
        return None

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_ffmpeg_path():
    """Find FFmpeg path from Winget installation"""
    try:
        local_app_data = os.environ.get('LOCALAPPDATA', '')
        if not local_app_data:
            return None
            
        # Search for ffmpeg.exe in Winget packages
        winget_dir = Path(local_app_data) / 'Microsoft/WinGet/Packages'
        if winget_dir.exists():
            for path in winget_dir.rglob('ffmpeg.exe'):
                return str(path.parent)
    except Exception:
        pass
    return None

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
    
    # Check for FFmpeg
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        opts['ffmpeg_location'] = ffmpeg_path
        print(f"✅ Found FFmpeg at: {ffmpeg_path}")
    
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
        
        # First check with extract_flat=True to quickly detect playlists
        ydl_opts = get_ydl_opts({'extract_flat': True})
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Check if it's a playlist
            if 'entries' in info:
                return jsonify({
                    'title': info.get('title', 'Unknown Playlist'),
                    'is_playlist': True,
                    'video_count': len(info.get('entries', []))
                })
        
        # If it's a single video, we need full details for formats
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
                'is_playlist': False
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<download_id>', methods=['GET'])
def get_progress(download_id):
    """Get progress for a specific download"""
    return jsonify(download_progress.get(download_id, {'status': 'starting', 'percent': 0}))

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video or audio in specified format"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('type', 'video')  # 'video' or 'audio'
        output_format = data.get('format', 'mp4')
        video_quality = data.get('quality', 'best')
        download_id = data.get('download_id')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
            
        # Allow user to select download folder
        download_path = select_download_folder()
        
        if not download_path:
            return jsonify({'error': 'Download cancelled: No folder selected'}), 400
            
        save_dir = Path(download_path)
        
        # Configure yt-dlp options
        ydl_opts = get_ydl_opts({
            'outtmpl': str(save_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'progress_hooks': [progress_hook],
        })
        
        if format_type == 'audio':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': '192',
            }]
        else:
            # Video download with quality selection
            if video_quality == 'best':
                # Best quality available up to 4K
                base_format = 'bestvideo[height<=2160]'
            else:
                # Specific quality (e.g., 1080, 720)
                base_format = f'bestvideo[height<={video_quality}]'
            
            # Combine video, audio, and fallback formats
            # Use specific ext if supported, otherwise convert
            if output_format == 'mp4':
                ydl_opts['format'] = f'{base_format}[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif output_format == 'webm':
                ydl_opts['format'] = f'{base_format}[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'
            else:
                ydl_opts['format'] = f'{base_format}+bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': output_format,
                }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Find the downloaded file
            if 'requested_downloads' in info:
                downloaded_file = info['requested_downloads'][0]['filepath']
                return jsonify({
                    'success': True,
                    'filename': os.path.basename(downloaded_file),
                    'path': downloaded_file,
                    'title': info.get('title', 'Unknown')
                })
            
            # Fallback: Check for the file with the correct extension
            title = sanitize_filename(info.get('title', 'video'))
            possible_files = list(save_dir.glob(f"{title}.*"))
            
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
                
    except DownloadError as e:
        error_msg = str(e)
        if "ffmpeg not found" in error_msg or "ffmpeg is not installed" in error_msg:
            return jsonify({
                'error': 'FFmpeg is missing! Please install it to download this format/quality. See FFMPEG_INSTALLATION.md for instructions.'
            }), 500
        return jsonify({'error': str(e)}), 500
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
        video_quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
            
        # Select download folder
        download_path = select_download_folder()
        
        if not download_path:
            return jsonify({'error': 'Download cancelled: No folder selected'}), 400
            
        save_dir = Path(download_path)
        
        # Create playlist subdirectory
        playlist_dir = save_dir / 'playlist_%(playlist_title)s'
        
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
            # Video download with quality selection
            if video_quality == 'best':
                base_format = 'bestvideo[height<=2160]'
            else:
                base_format = f'bestvideo[height<={video_quality}]'

            if output_format == 'mp4':
                ydl_opts['format'] = f'{base_format}[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif output_format == 'webm':
                ydl_opts['format'] = f'{base_format}[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'
            else:
                ydl_opts['format'] = f'{base_format}+bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': output_format,
                }]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            video_count = len(info.get('entries', []))
            playlist_title = sanitize_filename(info.get('title', 'Unknown Playlist'))
            
            return jsonify({
                'success': True,
                'video_count': video_count,
                'playlist_title': playlist_title,
                'download_path_name': f'downloads/playlist_{playlist_title}/'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-file')
def download_file():
    """Serve downloaded file from absolute path"""
    try:
        filepath = request.args.get('filepath')
        if not filepath:
            return jsonify({'error': 'Filepath is required'}), 400
            
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    print("🚀 SaveTube Server Starting...")
    # print("📁 Downloads will be saved to:", DOWNLOAD_DIR.absolute())
    print("🌐 Server running at: http://localhost:5000")
    print("\n⚠️  Make sure FFmpeg is installed for format conversion!")
    app.run(debug=True, port=5000, host='0.0.0.0')

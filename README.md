# SaveTube - YouTube Download Manager

![SaveTube Banner](https://img.shields.io/badge/SaveTube-YouTube%20Downloader-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A modern, feature-rich web application for downloading YouTube videos and extracting audio with support for multiple formats and playlist downloads.

## ✨ Features

- 🎥 **Video Downloads** - Download YouTube videos in multiple formats (MP4, WebM, AVI, MOV, MKV)
- 🎵 **Audio Extraction** - Extract audio from videos in various formats (MP3, WAV, M4A, OPUS, FLAC)
- 📋 **Playlist Support** - Download entire playlists at once
- 🎨 **Modern UI** - Beautiful dark theme with glassmorphism effects
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast & Reliable** - Powered by yt-dlp, the most reliable YouTube downloader
- 🔄 **Format Conversion** - Automatic format conversion using FFmpeg
- 📊 **Progress Tracking** - Real-time download progress indicators

## 🖼️ Screenshots

The application features a stunning dark theme with animated gradient backgrounds, glassmorphism cards, and smooth transitions for a premium user experience.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **FFmpeg** (Required for format conversion)
   - **Windows**: 
     - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
     - Extract and add to system PATH
     - Or use chocolatey: `choco install ffmpeg`
   - **macOS**: 
     - Use Homebrew: `brew install ffmpeg`
   - **Linux**: 
     - Ubuntu/Debian: `sudo apt install ffmpeg`
     - Fedora: `sudo dnf install ffmpeg`
   - Verify installation: `ffmpeg -version`

## 🚀 Installation

### Step 1: Clone or Download the Repository

```bash
cd "SaveTube-YouTube Download Manager"
```

### Step 2: Create a Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- flask-cors (Cross-Origin Resource Sharing)
- yt-dlp (YouTube downloader)

## 🎮 Usage

### Starting the Server

1. **Activate your virtual environment** (if not already activated)

2. **Run the Flask server:**
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

4. You should see the SaveTube interface with the animated background!

### Downloading Videos

1. **Enter a YouTube URL** in the input field
2. **Click "Get Info"** to fetch video metadata
3. **Preview the video** - thumbnail, title, and details will appear
4. **Choose your format:**
   - For video: Select from MP4, WebM, AVI, MOV, or MKV
   - For audio: Select from MP3, WAV, M4A, OPUS, or FLAC
5. **Click the download button** for your preferred option
6. **Wait for the download** - progress will be shown
7. **Find your file** in the `downloads` folder

### Downloading Playlists

1. **Enter a YouTube playlist URL**
2. **Click "Get Info"** - the app will detect it's a playlist
3. **Review playlist details** - number of videos and title
4. **Select format type** (Video or Audio)
5. **Choose output format**
6. **Click "Download Entire Playlist"**
7. **Wait for completion** - all videos will be downloaded to `downloads/playlist_[name]/`

## 📁 Project Structure

```
SaveTube-YouTube Download Manager/
├── app.py                 # Flask backend server
├── index.html            # Main HTML structure
├── style.css             # Modern CSS with glassmorphism
├── script.js             # Frontend JavaScript logic
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── downloads/           # Downloaded files (auto-created)
```

## 🎨 Supported Formats

### Video Formats
- **MP4** - Most compatible, recommended for general use
- **WebM** - Good quality, smaller file size
- **AVI** - High quality, larger file size
- **MOV** - Apple QuickTime format
- **MKV** - Matroska, supports multiple audio/subtitle tracks

### Audio Formats
- **MP3** - Most compatible, good quality
- **WAV** - Lossless, large file size
- **M4A** - AAC codec, good quality and compression
- **OPUS** - Modern codec, excellent quality/size ratio
- **FLAC** - Lossless compression

## ⚙️ Configuration

### Changing the Port

Edit `app.py` and modify the last line:
```python
app.run(debug=True, port=5000, host='0.0.0.0')  # Change port here
```

### Download Location

By default, files are saved to the `downloads` folder. To change this, edit `app.py`:
```python
DOWNLOAD_DIR = Path('your/custom/path')
```

## 🔧 Troubleshooting

### "FFmpeg not found" Error

**Problem:** Format conversion fails  
**Solution:** 
1. Install FFmpeg (see Prerequisites)
2. Add FFmpeg to your system PATH
3. Restart your terminal/command prompt
4. Verify with: `ffmpeg -version`

### "Connection refused" Error

**Problem:** Cannot connect to the server  
**Solution:**
1. Ensure the Flask server is running
2. Check if port 5000 is available
3. Try accessing `http://127.0.0.1:5000` instead

### "Invalid URL" Error

**Problem:** URL not recognized  
**Solution:**
1. Ensure you're using a valid YouTube URL
2. Supported formats:
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`
   - `https://www.youtube.com/playlist?list=PLAYLIST_ID`

### Download Fails

**Problem:** Download starts but fails  
**Solution:**
1. Check your internet connection
2. Verify the video is not private or restricted
3. Try updating yt-dlp: `pip install --upgrade yt-dlp`
4. Check the terminal for detailed error messages

### Slow Downloads

**Problem:** Downloads are very slow  
**Solution:**
1. This depends on your internet speed
2. YouTube may throttle download speeds
3. Try downloading during off-peak hours

## 🛡️ Legal Disclaimer

**IMPORTANT:** This tool is for **personal use only**. 

- ⚖️ Respect copyright laws in your jurisdiction
- 📜 Review YouTube's Terms of Service
- 🚫 Do not download copyrighted content without permission
- ✅ Only download content you have rights to or that is in the public domain

The developers of SaveTube are not responsible for any misuse of this software.

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **yt-dlp** - The powerful YouTube downloader library
- **Flask** - Lightweight web framework
- **FFmpeg** - Multimedia framework for format conversion

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the terminal output for error messages
3. Ensure all prerequisites are properly installed

## 🔄 Updates

To update yt-dlp to the latest version:
```bash
pip install --upgrade yt-dlp
```

To update all dependencies:
```bash
pip install --upgrade -r requirements.txt
```

---

**Made with ❤️ for the YouTube community**

*Remember: Download responsibly and respect content creators!*
#   y t - v i d e o - d o w n l o a d e r - S a v e T u b e  
 
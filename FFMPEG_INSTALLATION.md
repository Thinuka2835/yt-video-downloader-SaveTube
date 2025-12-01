# FFmpeg Installation Guide for SaveTube

## ⚠️ Error: FFmpeg Not Found

You're seeing this error because FFmpeg is not installed on your system:
```
ERROR: Postprocessing: ffprobe and ffmpeg not found
```

FFmpeg is **required** for:
- Converting video formats (AVI, MOV, MKV)
- Extracting audio (MP3, WAV, FLAC)
- Merging video and audio streams

---

## ✅ Quick Fix: Install FFmpeg

### **Option 1: Using Chocolatey (Recommended for Windows)**

1. **Install Chocolatey** (if not already installed):
   - Open PowerShell as Administrator
   - Run:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install FFmpeg**:
   ```powershell
   choco install ffmpeg -y
   ```

3. **Restart your terminal** and verify:
   ```powershell
   ffmpeg -version
   ```

---

### **Option 2: Manual Installation**

1. **Download FFmpeg**:
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`

2. **Extract the ZIP file**:
   - Extract to: `C:\ffmpeg`

3. **Add to PATH**:
   - Open System Properties → Environment Variables
   - Edit "Path" under System Variables
   - Add: `C:\ffmpeg\bin`
   - Click OK

4. **Restart your terminal** and verify:
   ```powershell
   ffmpeg -version
   ```

---

### **Option 3: Using Winget (Windows 11)**

```powershell
winget install ffmpeg
```

---

## 🔄 After Installing FFmpeg

1. **Close all terminals**
2. **Restart the SaveTube server**:
   ```bash
   python app.py
   ```
3. **Try downloading again**

---

## 📝 Formats That Work WITHOUT FFmpeg

If you don't want to install FFmpeg right now, you can still download:

### ✅ Works Without FFmpeg:
- **Video**: MP4, WebM (native formats)
- **Audio**: M4A, OPUS (native formats)

### ❌ Requires FFmpeg:
- **Video**: AVI, MOV, MKV (needs conversion)
- **Audio**: MP3, WAV, FLAC (needs extraction/conversion)

---

## 🎯 Quick Test

After installing FFmpeg, test with:

1. Select **MP4** format + any quality → Should work ✅
2. Select **MP3** audio → Should work ✅ (after FFmpeg install)
3. Select **AVI** format → Should work ✅ (after FFmpeg install)

---

## 🆘 Still Having Issues?

If FFmpeg is installed but still not working:

1. **Check if FFmpeg is in PATH**:
   ```powershell
   where.exe ffmpeg
   ```
   Should show: `C:\ffmpeg\bin\ffmpeg.exe` (or similar)

2. **Restart your computer** (to refresh PATH)

3. **Check FFmpeg version**:
   ```powershell
   ffmpeg -version
   ffprobe -version
   ```

---

## 💡 Pro Tip

For the **fastest downloads without FFmpeg**, use:
- **Video**: MP4 format (no conversion needed)
- **Audio**: M4A format (no conversion needed)

These formats download directly without post-processing!

---

*Last Updated: 2025-11-29*

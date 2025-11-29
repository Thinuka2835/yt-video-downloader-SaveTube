# 🔧 YouTube Bot Detection - Quick Fix Guide

## ⚠️ The Problem

YouTube has implemented strict bot detection that blocks automated downloads with errors like:
- "Sign in to confirm you're not a bot"
- "This helps protect our community"

This affects **ALL** yt-dlp based downloaders, not just SaveTube.

---

## ✅ Solution 1: Update yt-dlp (Try This First!)

YouTube frequently changes their API. Updating yt-dlp often fixes the issue:

```bash
pip install --upgrade yt-dlp
```

Then restart the SaveTube server:
```bash
python app.py
```

---

## ✅ Solution 2: Use YouTube Cookies (Most Reliable)

This method uses your browser's YouTube login session to bypass bot detection.

### Step-by-Step:

1. **Install a Cookie Export Extension**:
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Export Your YouTube Cookies**:
   - Go to [youtube.com](https://www.youtube.com) and make sure you're logged in
   - Click the extension icon
   - Click "Export" or "Download"
   - Save the file as `cookies.txt`

3. **Place cookies.txt in SaveTube Directory**:
   ```
   SaveTube-YouTube Download Manager/
   ├── app.py
   ├── cookies.txt  ← Put it here!
   ├── index.html
   └── ...
   ```

4. **Restart the Server**:
   ```bash
   python app.py
   ```
   
   You should see: `✅ Using cookies from: cookies.txt`

---

## ✅ Solution 3: Try Different Videos

Some videos work better than others:

✅ **More Likely to Work**:
- Public videos
- Non-age-restricted content
- Videos from verified channels
- Shorter videos (< 10 minutes)

❌ **Less Likely to Work**:
- Private or unlisted videos
- Age-restricted content
- Very long videos
- Recently uploaded videos

### Test Videos:
Try these known-working videos:
- `https://www.youtube.com/watch?v=dQw4w9WgXcQ` (Rick Astley - Never Gonna Give You Up)
- `https://www.youtube.com/watch?v=9bZkp7q19f0` (PSY - GANGNAM STYLE)

---

## ✅ Solution 4: Wait and Retry

If you're getting bot detection:

1. **Wait 5-10 minutes** - YouTube may have temporarily flagged your IP
2. **Close and reopen your browser**
3. **Try again** - The block is usually temporary

---

## ✅ Solution 5: Use Alternative URL Formats

Try different URL formats:

```
Standard: https://www.youtube.com/watch?v=VIDEO_ID
Short:    https://youtu.be/VIDEO_ID  
Mobile:   https://m.youtube.com/watch?v=VIDEO_ID
```

---

## 🔍 How to Check if It's Working

1. **Start the server**: `python app.py`
2. **Look for this message**:
   ```
   ℹ️  No cookies.txt found. See YOUTUBE_BOT_FIX.md for help
   ```
   OR
   ```
   ✅ Using cookies from: cookies.txt
   ```

3. **Try downloading a video**
4. **Check the terminal for errors**

---

## 🆘 Still Not Working?

### Check yt-dlp Version:
```bash
yt-dlp --version
```
Should be `2024.11.18` or newer.

### Check for Known Issues:
Visit: https://github.com/yt-dlp/yt-dlp/issues

### Try Manual Download (Test):
```bash
yt-dlp --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

If this works, SaveTube should work too!

---

## 📝 Technical Details

SaveTube now includes:
- ✅ Custom user agent spoofing
- ✅ Optimized HTTP headers
- ✅ Automatic cookie detection
- ✅ Retry logic (3 attempts)
- ✅ Fragment error handling
- ✅ Age gate bypass

---

## ⚖️ Legal Note

**Remember**: Only download content you have permission to download. Respect copyright laws and YouTube's Terms of Service.

---

## 💡 Pro Tips

1. **Keep yt-dlp Updated**: Run `pip install --upgrade yt-dlp` weekly
2. **Use Cookies**: This is the most reliable method
3. **Be Patient**: YouTube's bot detection changes frequently
4. **Test First**: Try a simple, public video before downloading playlists

---

**Need More Help?**

Check the main [README.md](README.md) for general usage instructions.

---

*Last Updated: November 2024*

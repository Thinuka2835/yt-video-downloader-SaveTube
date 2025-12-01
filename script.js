// API Configuration
const API_BASE = 'http://localhost:5000';

// DOM Elements
const youtubeUrlInput = document.getElementById('youtube-url');
const fetchInfoBtn = document.getElementById('fetch-info-btn');
const previewSection = document.getElementById('preview-section');
const downloadSection = document.getElementById('download-section');
const playlistSection = document.getElementById('playlist-section');
const progressSection = document.getElementById('progress-section');

// Video Info Elements
const videoThumbnail = document.getElementById('video-thumbnail');
const videoTitle = document.getElementById('video-title');
const videoUploader = document.getElementById('video-uploader');
const videoViews = document.getElementById('video-views');
const durationBadge = document.getElementById('duration-badge');

// Download Control Elements
const videoFormatSelect = document.getElementById('video-format');
const videoQualitySelect = document.getElementById('video-quality');
const downloadVideoBtn = document.getElementById('download-video-btn');
const audioFormatSelect = document.getElementById('audio-format');
const downloadAudioBtn = document.getElementById('download-audio-btn');

// Playlist Elements
const playlistInfo = document.getElementById('playlist-info');
const playlistFormatType = document.getElementById('playlist-format-type');
const playlistFormat = document.getElementById('playlist-format');
const downloadPlaylistBtn = document.getElementById('download-playlist-btn');

const progressTitle = document.getElementById('progress-title');
const progressStatus = document.getElementById('progress-status');
const progressFill = document.getElementById('progress-fill');

const notification = document.getElementById('notification');
const notificationMessage = document.getElementById('notification-message');
const notificationClose = document.getElementById('notification-close');

// State
let currentVideoInfo = null;
let currentPlaylistInfo = null;

// Statistics (reset on page refresh)
let successCount = 0;
let failCount = 0;

function updateStatsUI() {
    document.getElementById('success-count').textContent = successCount;
    document.getElementById('fail-count').textContent = failCount;
}

function incrementSuccess() {
    successCount++;
    updateStatsUI();
}

function incrementSuccessByCount(count) {
    successCount += count;
    updateStatsUI();
}

function incrementFail() {
    failCount++;
    updateStatsUI();
}

function incrementFailByCount(count) {
    failCount += count;
    updateStatsUI();
}

// Utility Functions
function formatDuration(seconds) {
    if (!seconds) return '0:00';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatViews(views) {
    if (!views) return '0 views';
    if (views >= 1000000) {
        return `${(views / 1000000).toFixed(1)}M views`;
    }
    if (views >= 1000) {
        return `${(views / 1000).toFixed(1)}K views`;
    }
    return `${views} views`;
}

function showNotification(message, type = 'info') {
    notification.className = `notification ${type}`;
    notificationMessage.textContent = message;
    notification.classList.remove('hidden');

    setTimeout(() => {
        notification.classList.add('hidden');
    }, 5000);
}

function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

function showProgress(title, status) {
    progressSection.classList.remove('hidden');
    progressTitle.textContent = title;
    progressStatus.textContent = status;
    progressFill.style.width = '0%';
}

function updateProgress(percent) {
    progressFill.style.width = `${percent}%`;
    if (percent >= 100) {
        progressStatus.textContent = 'Download complete!';
    }
}

function hideProgress() {
    progressSection.classList.add('hidden');
}

// Desktop Notifications
function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

function showDesktopNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification(title, {
            body: body,
            icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23FF6B6B"/><path d="M70 50L40 67.5V32.5L70 50Z" fill="white"/></svg>',
            badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23FF6B6B"/><path d="M70 50L40 67.5V32.5L70 50Z" fill="white"/></svg>'
        });

        // Auto-close after 5 seconds
        setTimeout(() => notification.close(), 5000);
    }
}

// Event Listeners
fetchInfoBtn.addEventListener('click', fetchVideoInfo);
downloadVideoBtn.addEventListener('click', () => downloadMedia('video'));
downloadAudioBtn.addEventListener('click', () => downloadMedia('audio'));
downloadPlaylistBtn.addEventListener('click', downloadPlaylist);
notificationClose.addEventListener('click', () => notification.classList.add('hidden'));

// Update playlist format options when type changes
playlistFormatType.addEventListener('change', (e) => {
    const type = e.target.value;
    playlistFormat.innerHTML = '';

    if (type === 'video') {
        playlistFormat.innerHTML = `
            <option value="mp4">MP4</option>
            <option value="webm">WebM</option>
            <option value="avi">AVI</option>
            <option value="mov">MOV</option>
            <option value="mkv">MKV</option>
        `;
    } else {
        playlistFormat.innerHTML = `
            <option value="mp3">MP3</option>
            <option value="wav">WAV</option>
            <option value="m4a">M4A</option>
            <option value="opus">OPUS</option>
            <option value="flac">FLAC</option>
        `;
    }
});

// Allow Enter key to fetch info
youtubeUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchVideoInfo();
    }
});

// Main Functions
async function fetchVideoInfo() {
    const url = youtubeUrlInput.value.trim();

    if (!url) {
        showNotification('Please enter a YouTube URL', 'error');
        return;
    }

    // Basic URL validation
    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        showNotification('Please enter a valid YouTube URL', 'error');
        return;
    }

    setButtonLoading(fetchInfoBtn, true);

    try {
        const response = await fetch(`${API_BASE}/api/video-info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch video info');
        }

        currentVideoInfo = data;

        // Check if it's a playlist
        if (data.is_playlist) {
            await fetchPlaylistInfo(url);
            // Don't display video info for playlist initially as it might be incomplete
        } else {
            displayVideoInfo(data);
            playlistSection.classList.add('hidden');
        }

        showNotification('Video info loaded successfully!', 'success');

    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
        previewSection.classList.add('hidden');
        downloadSection.classList.add('hidden');
        playlistSection.classList.add('hidden');
    } finally {
        setButtonLoading(fetchInfoBtn, false);
    }
}

async function fetchPlaylistInfo(url) {
    try {
        const response = await fetch(`${API_BASE}/api/playlist-info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch playlist info');
        }

        currentPlaylistInfo = data;
        displayPlaylistInfo(data);

    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
    }
}

function displayVideoInfo(data) {
    // Update thumbnail
    videoThumbnail.src = data.thumbnail;
    videoThumbnail.alt = data.title;

    // Update video details
    videoTitle.textContent = data.title;
    videoUploader.textContent = data.uploader;
    videoViews.textContent = formatViews(data.view_count);
    durationBadge.textContent = formatDuration(data.duration);

    // Show sections
    previewSection.classList.remove('hidden');
    downloadSection.classList.remove('hidden');

    // Scroll to preview
    previewSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayPlaylistInfo(data) {
    playlistInfo.textContent = `${data.video_count} videos in "${data.title}"`;
    playlistSection.classList.remove('hidden');

    // Also show first video info if available
    if (currentVideoInfo) {
        displayVideoInfo(currentVideoInfo);
    }

    // Scroll to playlist section
    playlistSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function downloadMedia(type) {
    const url = youtubeUrlInput.value.trim();

    if (!url) {
        showNotification('Please enter a YouTube URL', 'error');
        return;
    }

    const format = type === 'video' ? videoFormatSelect.value : audioFormatSelect.value;
    const quality = type === 'video' ? videoQualitySelect.value : 'best';
    const button = type === 'video' ? downloadVideoBtn : downloadAudioBtn;

    setButtonLoading(button, true);
    showProgress(
        `Downloading ${type}...`,
        `Preparing ${type} download in ${format.toUpperCase()} format`
    );

    try {
        // Simulate progress (for better user experience)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            updateProgress(progress);
        }, 500);

        try {
            const response = await fetch(`${API_BASE}/api/download`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url,
                    type,
                    format,
                    quality,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Download failed');
            }

            updateProgress(100);

            showNotification(
                `${type === 'video' ? 'Video' : 'Audio'} downloaded successfully! Starting file download...`,
                'success'
            );

            // Show desktop notification
            showDesktopNotification(
                'SaveTube - Download Complete',
                `${data.title} has been downloaded successfully!`
            );

            incrementSuccess();

            // === START: CRITICAL FIX TO TRIGGER BROWSER DOWNLOAD ===
            // === START: CRITICAL FIX TO TRIGGER BROWSER DOWNLOAD ===
            const downloadFileUrl = `${API_BASE}/api/download-file?filepath=${encodeURIComponent(data.path)}`;

            // Use a hidden anchor tag to trigger the file download in the browser
            const a = document.createElement('a');
            a.href = downloadFileUrl;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            // === END: CRITICAL FIX ===

            setTimeout(() => {
                hideProgress();
            }, 2000);
        } finally {
            clearInterval(progressInterval);
        }

    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
        hideProgress();
        incrementFail();
    } finally {
        setButtonLoading(button, false);
    }
}

async function downloadPlaylist() {
    const url = youtubeUrlInput.value.trim();

    if (!url) {
        showNotification('Please enter a YouTube URL', 'error');
        return;
    }

    if (!currentPlaylistInfo) {
        showNotification('Please fetch playlist info first', 'error');
        return;
    }

    const type = playlistFormatType.value;
    const format = playlistFormat.value;
    const quality = document.getElementById('playlist-quality').value;

    setButtonLoading(downloadPlaylistBtn, true);
    showProgress(
        'Downloading playlist...',
        `Preparing to download ${currentPlaylistInfo.video_count} videos`
    );

    try {
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 5;
            if (progress > 90) progress = 90;
            updateProgress(progress);
            progressStatus.textContent = `Downloading videos... (${Math.floor(progress)}%)`;
        }, 1000);

        const response = await fetch(`${API_BASE}/api/download-playlist`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url,
                type,
                format,
                quality
            }),
        });

        clearInterval(progressInterval);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Playlist download failed');
        }

        updateProgress(100);
        progressStatus.textContent = 'Playlist download complete!';

        showNotification(
            `Successfully downloaded ${data.video_count} videos from "${data.playlist_title}"! Files saved in: ${data.download_path_name}`,
            'success'
        );

        // Show desktop notification
        showDesktopNotification(
            'SaveTube - Playlist Download Complete',
            `Successfully downloaded ${data.video_count} videos from "${data.playlist_title}"!`
        );

        // Update statistics based on individual video results
        if (data.successful_count > 0) {
            incrementSuccessByCount(data.successful_count);
        }
        if (data.failed_count > 0) {
            incrementFailByCount(data.failed_count);
        }

        setTimeout(() => {
            hideProgress();
        }, 3000);

    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
        hideProgress();
        incrementFail();
    } finally {
        setButtonLoading(downloadPlaylistBtn, false);
    }
}

// Initialize
console.log('SaveTube initialized');
console.log('API Base:', API_BASE);

// Initialize stats
updateStatsUI();

// Request notification permission
requestNotificationPermission();

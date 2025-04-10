# YTDownload
# Media Downloader - Modern UI

A modern GUI application built with Python and `ttkbootstrap` to download videos from **YouTube** and **Twitter**. Features include subtitle support, audio-only mode, automatic thumbnail download, channel/profile organization, and progress tracking.

## 🔧 Features

- ✅ YouTube & Twitter video downloads
- 🎧 Audio-only (MP3) mode for YouTube
- 📝 Subtitle selection (English / Hindi)
- 🌐 Automatic resolution and best quality detection
- 📁 Organized folder structure:
  - `downloads_youtube/PROFILE_NAME/`
  - `downloads_twitter/PROFILE_NAME/`
- 📸 Auto-download best quality thumbnail
- 📊 Progress bar for individual and playlist downloads
- ✅ Clean modern UI using `ttkbootstrap`
- 🧠 Smart URL detection and format handling

## 📦 Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- ffmpeg (required for audio extraction)
- Python packages:
  - `ttkbootstrap`

Install the required Python packages using:

```bash
pip install ttkbootstrap



🚀 Usage
Run the App
bash
Copy
Edit
python yt_downloader_gui.py
Convert to Standalone .exe (Optional)
Use pyinstaller to generate an executable:

bash
Copy
Edit
pip install pyinstaller
pyinstaller --onefile --windowed yt_downloader_gui.py
Make sure to place yt-dlp.exe and ffmpeg.exe in the same folder as the final .exe.
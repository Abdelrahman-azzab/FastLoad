# FastLoad

A modern, user-friendly YouTube downloader for Windows that makes downloading videos and playlists extremely easy.

![FastLoad Screenshot](screenshot.png)

## 🚀 Features

- **Easy to Use**: Simply paste a YouTube link and click download
- **High Quality**: Download videos up to 8K resolution
- **Multiple Formats**: Supports MP4, MKV, WebM, MP3, WAV, and FLAC
- **Playlist Support**: Download entire playlists with one click
- **Progress Tracking**: Real-time download progress with speed indicators
- **Smart Detection**: Automatically detects YouTube URLs from clipboard
- **Modern UI**: Clean, intuitive interface designed for Windows

## 📋 System Requirements

- Windows 10 or later
- Internet connection
- Minimum 100MB free disk space

## 🔧 Installation

### Option 1: Download Executable (Recommended)
1. Download `FastLoad.exe` from the [releases page](https://github.com/fastload/fastload/releases)
2. Double-click to run - no installation required!

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/fastload/fastload.git
cd fastload

# Install dependencies
pip install -r requirements.txt

# Run the application
python fastload.py
```

### Option 3: Build Your Own Executable
```bash
# Install build dependencies
pip install -r requirements.txt

# Run the build script
python build.py
```

## 📖 How to Use

1. **Copy a YouTube URL**: Copy any YouTube video or playlist link
2. **Paste in FastLoad**: Click the "Paste Link" button
3. **Choose Quality & Format**: Select your preferred quality (up to 8K) and format
4. **Select Download Location**: Choose where to save your files
5. **Click Download**: Sit back and watch the progress!

### Supported URLs
- Individual videos: `https://youtube.com/watch?v=...`
- Playlists: `https://youtube.com/playlist?list=...`
- Short URLs: `https://youtu.be/...`
- Channel videos: `https://youtube.com/@channel`

### Quality Options
- **8K (2160p)**: Ultra-high definition (when available)
- **4K (2160p)**: 4K resolution
- **2K (1440p)**: QHD resolution
- **1080p**: Full HD
- **720p**: HD
- **480p, 360p, 240p**: Standard definitions
- **Best/Worst**: Automatic quality selection

### Format Options
- **Video**: MP4 (recommended), MKV, WebM
- **Audio**: MP3 (most compatible), WAV (lossless), FLAC (lossless)

## 🛠️ Development

### Project Structure
```
fastload/
├── fastload.py          # Main application
├── build.py            # Build script for executable
├── setup.py            # Python package setup
├── requirements.txt    # Dependencies
├── README.md          # This file
└── installer/         # Built files directory
    ├── FastLoad.exe   # Windows executable
    ├── Installation_Guide.txt
    └── version.txt
```

### Building the Application

To build a Windows executable:
```bash
python build.py
```

This will create:
- `dist/FastLoad.exe` - The standalone executable
- `installer/` directory with all distribution files

### Dependencies
- **yt-dlp**: YouTube download engine
- **tkinter**: GUI framework (built into Python)
- **threading**: Background downloads
- **PyInstaller**: Executable building (dev dependency)

## 🐛 Troubleshooting

### Common Issues

**"Invalid URL" Error**
- Ensure you're using a valid YouTube URL
- Check that the video is publicly available

**Download Fails**
- Check your internet connection
- Try a different quality/format
- Some videos may be region-locked

**Slow Downloads**
- Download speed depends on your internet connection
- Try downloading during off-peak hours
- Consider lowering the video quality

**Application Won't Start**
- Make sure you have Windows 10 or later
- Try running as administrator
- Check Windows Defender hasn't quarantined the file

### Getting Help
If you encounter issues:
1. Check the application log for error details
2. Try downloading a different video to isolate the issue
3. Report bugs on our [GitHub Issues](https://github.com/fastload/fastload/issues) page

## ⚖️ Legal Notice

**Important**: Please respect copyright laws and YouTube's Terms of Service when using FastLoad. Only download content that you have permission to download or that is in the public domain.

FastLoad is provided for educational and personal use only. Users are responsible for ensuring their use complies with applicable laws and terms of service.

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful YouTube download engine
- GUI built with Python's tkinter
- Icons and design inspired by modern Windows applications

---

**FastLoad** - Making YouTube downloads fast, easy, and reliable! 🚀
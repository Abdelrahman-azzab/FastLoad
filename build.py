#!/usr/bin/env python3
"""
Build script for FastLoad Windows executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build Windows executable using PyInstaller"""
    print("Building FastLoad Windows executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=FastLoad',
        '--onefile',
        '--windowed',
        '--icon=icon.ico',  # You can add an icon file
        '--add-data=requirements.txt;.',
        '--hidden-import=yt_dlp',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=threading',
        '--exclude-module=_tkinter',
        '--exclude-module=tkinter.test',
        'fastload.py'
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created at: dist/FastLoad.exe")
        
        # Create installer directory
        installer_dir = Path("installer")
        installer_dir.mkdir(exist_ok=True)
        
        # Copy executable to installer directory
        if Path("dist/FastLoad.exe").exists():
            shutil.copy2("dist/FastLoad.exe", installer_dir)
            print(f"Executable copied to: {installer_dir}/FastLoad.exe")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Please install it with: pip install pyinstaller")
        return False

def create_installer_files():
    """Create additional installer files"""
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Create installation guide
    install_guide = """# FastLoad Installation Guide

## System Requirements
- Windows 10 or later
- Internet connection for downloading videos

## Installation Steps
1. Download FastLoad.exe from the official website
2. Double-click FastLoad.exe to run the application
3. No additional installation required!

## How to Use FastLoad

### Quick Start
1. Copy a YouTube video or playlist URL
2. Click "Paste Link" in FastLoad
3. Select your desired quality and format
4. Click "Download"

### Supported Formats
- **Video**: MP4, MKV, WebM
- **Audio**: MP3, WAV, FLAC

### Quality Options
- Up to 8K (2160p) for supported videos
- 4K (2160p), 2K (1440p), 1080p, 720p, 480p, 360p, 240p
- Best quality (automatic selection)

### Features
- Download individual videos or entire playlists
- Real-time download progress tracking
- Automatic file organization
- Clipboard integration for easy URL pasting
- Error handling and detailed logging

## Troubleshooting

### Common Issues
- **"Invalid URL" error**: Make sure you're using a valid YouTube URL
- **Download fails**: Check your internet connection and try again
- **No audio in video**: Try selecting a different format

### Contact Support
For additional help, visit our website or contact support.

## Legal Notice
Please respect copyright laws and YouTube's Terms of Service when using FastLoad.
Only download content you have permission to download.
"""
    
    with open(installer_dir / "Installation_Guide.txt", "w", encoding="utf-8") as f:
        f.write(install_guide)
    
    # Create version info
    version_info = """FastLoad v1.0.0

A modern, user-friendly YouTube downloader for Windows.

Features:
- Download videos and playlists from YouTube
- Support for multiple quality options up to 8K
- Multiple format support (MP4, MKV, MP3, etc.)
- Real-time progress tracking
- Easy-to-use interface

Build Date: Generated automatically
"""
    
    with open(installer_dir / "version.txt", "w") as f:
        f.write(version_info)
    
    print("Installer files created successfully!")

if __name__ == "__main__":
    print("FastLoad Build System")
    print("===================")
    
    # Check if we're on Windows or have wine for cross-compilation
    if sys.platform != "win32":
        print("Warning: Building on non-Windows system. The executable may not work properly.")
        print("Consider building on Windows or using a Windows virtual machine.")
    
    # Create installer files
    create_installer_files()
    
    # Build executable
    if build_executable():
        print("\n✅ Build completed successfully!")
        print("📁 Files created in 'installer/' directory:")
        installer_dir = Path("installer")
        for file in installer_dir.iterdir():
            print(f"   - {file.name}")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)
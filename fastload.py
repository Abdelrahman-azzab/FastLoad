#!/usr/bin/env python3
"""
FastLoad - Desktop YouTube Downloader
A modern, user-friendly YouTube video and playlist downloader for Windows.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
import re
import subprocess
from pathlib import Path
import yt_dlp
from urllib.parse import urlparse
import json

class FastLoadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastLoad - YouTube Downloader")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set application icon and styling
        self.setup_styling()
        
        # Initialize variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads" / "FastLoad"))
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="best")
        self.format_var = tk.StringVar(value="mp4")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to download")
        
        # Create GUI
        self.create_widgets()
        
        # Ensure download directory exists
        os.makedirs(self.download_path.get(), exist_ok=True)
    
    def setup_styling(self):
        """Configure the application styling"""
        self.root.configure(bg='#f0f0f0')
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Segoe UI', 10, 'bold'), background='#f0f0f0')
        style.configure('Download.TButton', font=('Segoe UI', 12, 'bold'))
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="FastLoad", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="Video/Playlist URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Segoe UI', 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        paste_btn = ttk.Button(url_frame, text="Paste Link", command=self.paste_link)
        paste_btn.grid(row=0, column=1)
        
        # Quality and Format Selection
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Quality selection
        ttk.Label(options_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var, state="readonly", width=15)
        quality_combo['values'] = ('best', '2160p (4K)', '1440p (2K)', '1080p', '720p', '480p', '360p', '240p', 'worst')
        quality_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Format selection
        ttk.Label(options_frame, text="Format:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, state="readonly", width=10)
        format_combo['values'] = ('mp4', 'mkv', 'webm', 'mp3', 'wav', 'flac')
        format_combo.grid(row=0, column=3)
        
        # Download path selection
        path_frame = ttk.LabelFrame(main_frame, text="Download Location", padding="10")
        path_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        path_frame.columnconfigure(0, weight=1)
        
        path_entry = ttk.Entry(path_frame, textvariable=self.download_path, font=('Segoe UI', 10))
        path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download", style='Download.TButton', 
                                      command=self.start_download)
        self.download_btn.grid(row=4, column=0, columnspan=3, pady=(0, 20))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Download Progress", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, font=('Consolas', 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def paste_link(self):
        """Paste URL from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            if self.is_valid_youtube_url(clipboard_content):
                self.url_var.set(clipboard_content)
                self.log_message(f"Pasted URL: {clipboard_content}")
            else:
                messagebox.showwarning("Invalid URL", "Clipboard doesn't contain a valid YouTube URL")
        except tk.TclError:
            messagebox.showerror("Error", "Clipboard is empty or contains non-text data")
    
    def is_valid_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
            r'(?:https?://)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/channel/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/@[\w-]+',
        ]
        return any(re.match(pattern, url.strip()) for pattern in youtube_patterns)
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def progress_hook(self, d):
        """Handle download progress updates"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_var.set(percent)
                speed = d.get('speed', 0)
                speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "Unknown"
                self.status_var.set(f"Downloading... {percent:.1f}% - {speed_str}")
            elif '_percent_str' in d:
                percent_str = d['_percent_str'].strip()
                self.status_var.set(f"Downloading... {percent_str}")
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            filename = os.path.basename(d['filename'])
            self.status_var.set(f"Completed: {filename}")
            self.log_message(f"Downloaded: {filename}")
    
    def get_ydl_opts(self):
        """Get yt-dlp options based on user selection"""
        format_quality = self.quality_var.get()
        file_format = self.format_var.get()
        
        # Map quality selections to yt-dlp format strings
        quality_map = {
            'best': 'best',
            '2160p (4K)': 'best[height<=2160]',
            '1440p (2K)': 'best[height<=1440]',
            '1080p': 'best[height<=1080]',
            '720p': 'best[height<=720]',
            '480p': 'best[height<=480]',
            '360p': 'best[height<=360]',
            '240p': 'best[height<=240]',
            'worst': 'worst'
        }
        
        format_str = quality_map.get(format_quality, 'best')
        
        # Handle audio-only formats
        if file_format in ['mp3', 'wav', 'flac']:
            format_str = 'bestaudio'
        
        opts = {
            'format': format_str,
            'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'no_warnings': False,
        }
        
        # Post-processing for audio formats
        if file_format in ['mp3', 'wav', 'flac']:
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': file_format,
                'preferredquality': '192' if file_format == 'mp3' else None,
            }]
        
        return opts
    
    def download_video(self):
        """Download video/playlist in separate thread"""
        url = self.url_var.get().strip()
        
        if not url:
            self.log_message("Error: Please enter a URL")
            return
        
        if not self.is_valid_youtube_url(url):
            self.log_message("Error: Invalid YouTube URL")
            return
        
        try:
            self.download_btn.configure(state='disabled', text='Downloading...')
            self.progress_var.set(0)
            self.status_var.set("Preparing download...")
            self.log_message(f"Starting download: {url}")
            
            # Ensure download directory exists
            os.makedirs(self.download_path.get(), exist_ok=True)
            
            opts = self.get_ydl_opts()
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Get video info first
                self.log_message("Fetching video information...")
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:  # Playlist
                    self.log_message(f"Found playlist with {len(info['entries'])} videos")
                else:  # Single video
                    self.log_message(f"Video title: {info.get('title', 'Unknown')}")
                
                # Start actual download
                ydl.download([url])
            
            self.progress_var.set(100)
            self.status_var.set("Download completed successfully!")
            self.log_message("All downloads completed!")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            self.status_var.set("Download failed")
            messagebox.showerror("Download Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.download_btn.configure(state='normal', text='Download')
    
    def start_download(self):
        """Start download in background thread"""
        thread = threading.Thread(target=self.download_video)
        thread.daemon = True
        thread.start()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = FastLoadApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
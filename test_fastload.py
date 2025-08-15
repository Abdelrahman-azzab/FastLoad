#!/usr/bin/env python3
"""
Test script for FastLoad application
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastload import FastLoadApp

class TestFastLoad(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.root = tk.Tk()
        self.app = FastLoadApp(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()
    
    def test_initialization(self):
        """Test that the app initializes correctly"""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.root.title(), "FastLoad - YouTube Downloader")
        self.assertEqual(self.app.quality_var.get(), "best")
        self.assertEqual(self.app.format_var.get(), "mp4")
    
    def test_youtube_url_validation(self):
        """Test YouTube URL validation"""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMGJn3eOAlaT9nHyig",
            "youtube.com/watch?v=dQw4w9WgXcQ",
            "youtu.be/dQw4w9WgXcQ"
        ]
        
        invalid_urls = [
            "https://www.google.com",
            "not a url",
            "https://vimeo.com/123456789",
            "",
            "youtube.com"
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(self.app.is_valid_youtube_url(url), f"URL should be valid: {url}")
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(self.app.is_valid_youtube_url(url), f"URL should be invalid: {url}")
    
    def test_ydl_options_generation(self):
        """Test yt-dlp options generation"""
        # Test default options
        opts = self.app.get_ydl_opts()
        self.assertEqual(opts['format'], 'best')
        self.assertIn('progress_hooks', opts)
        
        # Test quality selection
        self.app.quality_var.set('1080p')
        opts = self.app.get_ydl_opts()
        self.assertEqual(opts['format'], 'best[height<=1080]')
        
        # Test audio format
        self.app.format_var.set('mp3')
        opts = self.app.get_ydl_opts()
        self.assertEqual(opts['format'], 'bestaudio')
        self.assertIn('postprocessors', opts)
        self.assertEqual(opts['postprocessors'][0]['preferredcodec'], 'mp3')
    
    @patch('fastload.tk.Tk.clipboard_get')
    def test_paste_link_functionality(self, mock_clipboard):
        """Test paste link functionality"""
        # Test valid URL
        mock_clipboard.return_value = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.app.paste_link()
        self.assertEqual(self.app.url_var.get(), "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        # Test invalid URL
        mock_clipboard.return_value = "https://www.google.com"
        with patch('fastload.messagebox.showwarning') as mock_warning:
            self.app.paste_link()
            mock_warning.assert_called_once()
    
    def test_log_message(self):
        """Test log message functionality"""
        test_message = "Test log message"
        self.app.log_message(test_message)
        
        # Get the content of the log text widget
        log_content = self.app.log_text.get("1.0", tk.END)
        self.assertIn(test_message, log_content)

def run_gui_test():
    """Run a basic GUI test"""
    print("Starting GUI test...")
    root = tk.Tk()
    app = FastLoadApp(root)
    
    # Test window properties
    print(f"✅ Window title: {root.title()}")
    print(f"✅ Window geometry: {root.geometry()}")
    
    # Test that all main widgets exist
    widgets_to_check = [
        'url_entry', 'download_btn', 'progress_bar', 
        'status_label', 'log_text'
    ]
    
    for widget_name in widgets_to_check:
        widget = getattr(app, widget_name, None)
        if widget:
            print(f"✅ Widget {widget_name} exists")
        else:
            print(f"❌ Widget {widget_name} missing")
    
    # Test URL validation
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.google.com"
    ]
    
    for url in test_urls:
        is_valid = app.is_valid_youtube_url(url)
        print(f"✅ URL validation for {url}: {'Valid' if is_valid else 'Invalid'}")
    
    print("GUI test completed. Close the window to continue.")
    
    # Show the window briefly
    root.after(3000, root.destroy)  # Auto-close after 3 seconds
    root.mainloop()

if __name__ == "__main__":
    print("FastLoad Test Suite")
    print("==================")
    
    # Run unit tests
    print("\n1. Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run GUI test
    print("\n2. Running GUI test...")
    run_gui_test()
    
    print("\n✅ All tests completed!")
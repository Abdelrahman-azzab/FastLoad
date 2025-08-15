from setuptools import setup, find_packages

setup(
    name="FastLoad",
    version="1.0.0",
    description="A modern, user-friendly YouTube downloader for Windows",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="FastLoad Team",
    author_email="support@fastload.app",
    url="https://github.com/fastload/fastload",
    py_modules=["fastload"],
    install_requires=[
        "yt-dlp>=2024.1.7",
        "tkinter-dnd2>=0.3.0",
        "Pillow>=10.2.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "build": ["pyinstaller>=6.3.0"],
    },
    entry_points={
        "console_scripts": [
            "fastload=fastload:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    keywords="youtube downloader video audio playlist mp4 mp3 gui windows",
    project_urls={
        "Bug Reports": "https://github.com/fastload/fastload/issues",
        "Source": "https://github.com/fastload/fastload",
        "Documentation": "https://fastload.app/docs",
    },
)
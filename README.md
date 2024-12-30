# Faceless Video Generator 🎥🤫

## Overview
A cross-platform tool for generating engaging social media videos with AI-generated content and optional subtitles.

## Prerequisites
- Python 3.8+
- `pip` package manager

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/faceless-video-generator.git
cd faceless-video-generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Optional: ImageMagick Installation
For advanced subtitle rendering, install ImageMagick:
```bash
python install_imagemagick.py
```

## Usage

### Generate Video
```bash
python video_generator.py
```

### Generate Video with Subtitles
```bash
python subtitle_generator.py
```

## Troubleshooting
- If subtitle generation fails, ensure ImageMagick is installed
- Check `output/` directory for generated videos
- Verify all dependencies are correctly installed

## Known Limitations
- Current version has simplified subtitle rendering
- Word-by-word subtitles may not work on all platforms

## Contributing
PRs welcome! Please read `CONTRIBUTING.md` for guidelines.

## License
MIT License

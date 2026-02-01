# 🎬 Video Piracy Detection System

A hackathon-friendly Python solution that detects whether a recorded video is a pirated copy of an original video using perceptual image similarity and audio spectrogram matching.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **FFmpeg** installed and in PATH
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Usage

1. Place your video files in the project directory:
   - `originalvideo.mp4` (the original content)
   - `recordedvideo.mp4` (the potentially pirated content)

2. Run the detection system:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
CineTry/
├── config.py              # Configuration constants
├── utils.py               # FFmpeg wrapper utilities
├── reference_extractor.py # Phase 1: Extract from original
├── recorded_extractor.py  # Phase 2: Extract from recorded
├── comparator.py          # Phase 3: Compare & decide
├── main.py                # Main orchestrator
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── output/                # Generated during execution
    ├── reference/         # Original screenshots & audio
    ├── recorded/          # Recorded screenshots & audio
    ├── metadata.json      # Extraction metadata
    └── results.json       # Detection results
```

## 🔍 How It Works

### Phase 1: Reference Generation
- Automatically selects random timestamps from the original video
- Extracts screenshots at those timestamps
- Extracts 15-second audio clips starting from those timestamps
- Saves metadata to JSON

### Phase 2: Recorded Video Extraction
- Reads timestamps from metadata
- Extracts screenshots and audio from the recorded video at the same timestamps

### Phase 3: Comparison & Decision
- **Image Comparison**: Uses perceptual hashing (pHash) to compare screenshots
  - Calculates Hamming distance between hashes
  - Threshold: distance ≤ 10 = match
- **Audio Comparison**: Uses mel spectrogram + cosine similarity
  - Threshold: similarity ≥ 0.7 = match
- **Decision Logic**:
  - If ≥50% screenshots match → **PIRATED**
  - Else if audio similarity is high → **PIRATED**
  - Else → **NOT PIRATED**

## ⚙️ Configuration

Edit `config.py` to customize:

```python
NUM_SAMPLES = 4              # Number of random timestamps
AUDIO_DURATION = 15          # Audio clip duration (seconds)
IMAGE_HASH_THRESHOLD = 10    # Image similarity threshold
AUDIO_SIMILARITY_THRESHOLD = 0.7  # Audio similarity threshold
SCREENSHOT_MATCH_PERCENTAGE = 0.5  # 50% match required
```

## 📊 Example Output

```
==================================================
🎬 Video Piracy Detection System
==================================================

📂 Loading originalvideo.mp4...
   Duration: 04:05 (245.3s)
🎲 Generated random timestamps: [32, 88, 145, 210]

Phase 1: Extracting reference data...
  ✓ Screenshot at 32s
  ✓ Audio clip at 32s (15s duration)
  ✓ Screenshot at 88s
  ✓ Audio clip at 88s (15s duration)
  ✓ Screenshot at 145s
  ✓ Audio clip at 145s (15s duration)
  ✓ Screenshot at 210s
  ✓ Audio clip at 210s (15s duration)
💾 Metadata saved to output/metadata.json

Phase 2: Extracting from recorded video...
📂 Loaded recordedvideo.mp4
  ✓ Screenshot at 32s
  ✓ Audio clip at 32s (15s duration)
  ✓ Screenshot at 88s
  ✓ Audio clip at 88s (15s duration)
  ✓ Screenshot at 145s
  ✓ Audio clip at 145s (15s duration)
  ✓ Screenshot at 210s
  ✓ Audio clip at 210s (15s duration)

Phase 3: Comparing content...
🖼️  Visual match: 3 / 4 (75.0%)
🔊 Audio similarity: HIGH (avg: 0.85)

==================================================
🚨 RESULT: PIRATED
==================================================

Reason: Visual match 75.0% >= 50.0%

📄 Detailed results saved to output/results.json
```

## 🛠️ Testing Individual Modules

Each module can be tested independently:

```bash
# Test Phase 1 only
python reference_extractor.py

# Test Phase 2 only (requires Phase 1 to run first)
python recorded_extractor.py

# Test Phase 3 only (requires Phase 1 & 2 to run first)
python comparator.py
```

## 🎯 Key Features

- ✅ **No external APIs** - Everything runs locally
- ✅ **No deep learning** - Uses classical signal processing
- ✅ **Perceptual comparison** - Not pixel-perfect matching
- ✅ **Robust to screen recording** - Handles compression, scaling, etc.
- ✅ **Demo-friendly output** - Clear, colorful console logs
- ✅ **Modular design** - Easy to understand and modify
- ✅ **Error handling** - Graceful failures with helpful messages

## 📝 Notes

- The system uses **perceptual hashing** for images, which is robust to minor changes like compression, scaling, and color adjustments
- **Audio comparison** uses mel spectrograms, which capture the perceptual characteristics of sound
- Random timestamps help avoid false positives from common intro/outro sequences
- The system automatically handles videos of different lengths

## 🐛 Troubleshooting

**"FFmpeg not found"**
- Ensure FFmpeg is installed and in your system PATH
- Test with: `ffmpeg -version`

**"No reference samples were extracted"**
- Check that `originalvideo.mp4` exists and is a valid video file
- Ensure FFmpeg can read the video format

**Low detection accuracy**
- Adjust thresholds in `config.py`
- Increase `NUM_SAMPLES` for more comparison points
- Check that videos are actually related

## 📄 License

MIT License - Free for hackathon use!

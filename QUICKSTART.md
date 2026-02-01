# 🎬 Quick Start Guide

## Prerequisites Check

1. **FFmpeg Installation** (REQUIRED):
   ```bash
   # Check if FFmpeg is installed
   ffmpeg -version
   ffprobe -version
   
   # If not installed:
   # Ubuntu/Debian: sudo apt install ffmpeg
   # macOS: brew install ffmpeg
   # Windows: Download from https://ffmpeg.org/download.html
   ```

2. **Python Dependencies** (ALREADY INSTALLED ✅):
   ```bash
   pip install -r requirements.txt
   ```

## Running the Detection System

### Step 1: Add Your Video Files

Place these files in `/home/siddu/MyProJects/Competions/CineTry/`:
- `originalvideo.mp4` - The original content
- `recordedvideo.mp4` - The potentially pirated content

### Step 2: Run the System

```bash
cd /home/siddu/MyProJects/Competions/CineTry
python main.py
```

### Step 3: Review Results

The system will:
1. Extract reference data from the original video
2. Extract matching data from the recorded video
3. Compare using perceptual hashing and audio similarity
4. Display the verdict: **PIRATED** or **NOT PIRATED**

Results are saved to:
- `output/metadata.json` - Extraction metadata
- `output/results.json` - Detailed comparison results
- `output/reference/` - Original screenshots and audio
- `output/recorded/` - Recorded screenshots and audio

## Testing Individual Phases

```bash
# Test Phase 1 only (reference extraction)
python reference_extractor.py

# Test Phase 2 only (recorded extraction)
python recorded_extractor.py

# Test Phase 3 only (comparison)
python comparator.py
```

## Customization

Edit `config.py` to adjust:
- Number of samples: `NUM_SAMPLES = 4`
- Audio duration: `AUDIO_DURATION = 15`
- Image threshold: `IMAGE_HASH_THRESHOLD = 10`
- Audio threshold: `AUDIO_SIMILARITY_THRESHOLD = 0.7`
- Match percentage: `SCREENSHOT_MATCH_PERCENTAGE = 0.5`

## Troubleshooting

**"FFmpeg not found"**
→ Install FFmpeg and ensure it's in your PATH

**"Video file not found"**
→ Ensure video files are named exactly `originalvideo.mp4` and `recordedvideo.mp4`

**"No samples extracted"**
→ Check that video files are valid and FFmpeg can read them

## Demo Tips

For a hackathon demo:
1. Use short videos (1-2 minutes) for faster processing
2. The console output is colorful and demo-friendly
3. Show the generated screenshots side-by-side
4. Explain the perceptual hashing concept
5. Demonstrate robustness by testing with compressed/scaled videos

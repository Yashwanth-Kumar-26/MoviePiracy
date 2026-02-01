# 🎯 Threshold Tuning Guide

## Understanding the Thresholds

The detection system uses three key thresholds that can be adjusted in `config.py`:

### 1. IMAGE_HASH_THRESHOLD
- **What it is**: Maximum Hamming distance between perceptual hashes
- **Range**: 0-64 (lower = more strict)
- **Current**: 30
- **How it works**: Compares structural similarity of images
  - Distance 0-10: Nearly identical
  - Distance 10-20: Very similar (same content, minor changes)
  - Distance 20-30: Similar (screen recording with compression)
  - Distance 30+: Different content or heavy modifications

### 2. AUDIO_SIMILARITY_THRESHOLD
- **What it is**: Minimum cosine similarity between audio spectrograms
- **Range**: 0.0-1.0 (higher = more strict)
- **Current**: 0.25
- **How it works**: Compares audio frequency patterns
  - 0.8-1.0: Nearly identical audio
  - 0.5-0.8: Very similar (same content, minor compression)
  - 0.25-0.5: Similar (screen recording with audio compression)
  - 0.0-0.25: Different audio or heavy modifications

### 3. SCREENSHOT_MATCH_PERCENTAGE
- **What it is**: Minimum percentage of screenshots that must match
- **Range**: 0.0-1.0 (higher = more strict)
- **Current**: 0.25 (25%)
- **How it works**: Determines how many samples need to match
  - With 4 samples: 0.25 = 1 match, 0.5 = 2 matches, 0.75 = 3 matches

---

## Recommended Settings by Use Case

### 🎯 High Quality Pirated Copies
**Scenario**: Direct file copies, minimal compression
```python
IMAGE_HASH_THRESHOLD = 10
AUDIO_SIMILARITY_THRESHOLD = 0.7
SCREENSHOT_MATCH_PERCENTAGE = 0.5
```

### 📹 Screen Recordings (Current)
**Scenario**: Screen-captured videos with compression
```python
IMAGE_HASH_THRESHOLD = 30
AUDIO_SIMILARITY_THRESHOLD = 0.25
SCREENSHOT_MATCH_PERCENTAGE = 0.25
```

### 🗜️ Heavily Compressed Videos
**Scenario**: Re-encoded multiple times, watermarks added
```python
IMAGE_HASH_THRESHOLD = 35
AUDIO_SIMILARITY_THRESHOLD = 0.20
SCREENSHOT_MATCH_PERCENTAGE = 0.20
```

### 🔒 Strict Detection (Minimize False Positives)
**Scenario**: Only flag very obvious copies
```python
IMAGE_HASH_THRESHOLD = 8
AUDIO_SIMILARITY_THRESHOLD = 0.8
SCREENSHOT_MATCH_PERCENTAGE = 0.6
```

### 🌐 Lenient Detection (Catch More Cases)
**Scenario**: Detect even heavily modified videos
```python
IMAGE_HASH_THRESHOLD = 40
AUDIO_SIMILARITY_THRESHOLD = 0.15
SCREENSHOT_MATCH_PERCENTAGE = 0.15
```

---

## How to Tune for Your Videos

1. **Run with debug output** (already enabled):
   ```bash
   python main.py
   ```

2. **Check the detailed comparison results**:
   - Look at individual hash distances
   - Look at individual audio similarities

3. **Adjust thresholds**:
   - If hash distances are consistently above threshold → increase `IMAGE_HASH_THRESHOLD`
   - If audio similarities are consistently below threshold → decrease `AUDIO_SIMILARITY_THRESHOLD`
   - If too few samples match → decrease `SCREENSHOT_MATCH_PERCENTAGE`

4. **Test again** and iterate until detection works correctly

---

## Example Debug Output Analysis

```
Sample 0 @ 29s:
  Image Hash Distance: 26 (threshold: 30) - ✓ MATCH
  Audio Similarity: 0.131 (threshold: 0.25) - ✗ NO MATCH
```

**Analysis**:
- Hash distance 26 is close to threshold 30 → threshold is appropriate
- Audio similarity 0.131 is below 0.25 → this sample doesn't match on audio
- Overall: 1 out of 2 metrics matched for this sample

---

## Tips

- **Start conservative**: Begin with stricter thresholds and relax if needed
- **Use multiple samples**: Increase `NUM_SAMPLES` (in config.py) for more reliable detection
- **Balance metrics**: Don't rely on just one metric (image or audio)
- **Test with real data**: Use actual pirated and non-pirated videos to calibrate
- **Consider false positives**: Very lenient thresholds may flag unrelated videos

---

## Current Configuration Performance

With current settings:
- ✅ Detects screen-recorded videos
- ✅ Handles compression artifacts
- ✅ Tolerates watermarks and overlays
- ⚠️ May have false positives with very similar but different content
- ⚠️ May miss heavily edited videos (cropped, color-graded, etc.)

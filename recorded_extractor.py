"""
Phase 2: Recorded Video Extraction Module
Extracts screenshots and audio clips from the recorded video at the same timestamps
"""

import os
import json
from typing import Dict
import config
import utils


def extract_recorded_data(video_path: str, metadata: Dict) -> Dict:
    """
    Extract screenshots and audio clips from recorded video using reference timestamps
    
    Args:
        video_path: Path to the recorded video
        metadata: Metadata from reference extraction (contains timestamps)
        
    Returns:
        Updated metadata with recorded video information
    """
    print(f"\nPhase 2: Extracting from recorded video...")
    print(f"📂 Loaded {video_path}")
    
    # Get recorded video duration
    duration = utils.get_video_duration(video_path)
    if duration is None:
        raise ValueError(f"Failed to get duration for {video_path}")
    
    # Create output directory
    utils.ensure_directory(config.RECORDED_DIR)
    
    # NEW: Audio Sync
    # We need to find the offset of recorded video relative to reference
    # using the anchors in metadata['anchors'] or if not present, assume 0.
    import audio_sync
    # Pass extracted anchors from metadata
    ref_anchors = metadata.get("anchors", [])
    offset = audio_sync.get_consensus_offset(metadata["original_video"], video_path, anchors=ref_anchors)
    
    print(f"⏱ Applying Time Offset: {offset:.2f}s")
    
    # Extract at the same timestamps (Adjusted by offset)
    timestamps = metadata["timestamps"]
    recorded_samples = []
    
    for i, ref_timestamp in enumerate(timestamps):
        # Calculate where this timestamp is in the recorded video
        # Rec_Time = Ref_Time - Offset
        # e.g. If Ref is 100s, and Offset is 10s (Recorded starts at 10s of Ref),
        # Then Rec_Time = 100 - 10 = 90s.
        
        # Correction: 
        # offset = anchor_time_ref - match_time_rec
        # So match_time_rec = anchor_time_ref - offset
        # This formula holds generally.
        rec_timestamp = ref_timestamp - offset
        
        if rec_timestamp < 0:
            print(f"  ⚠ Timestamp {int(ref_timestamp)}s is before start of recorded video (rec_time={int(rec_timestamp)}s)")
            continue
            
        # Check if timestamp is within recorded video duration
        if rec_timestamp > duration:
            print(f"  ⚠ Skipping timestamp {int(ref_timestamp)}s (rec_time={int(rec_timestamp)}s > duration)")
            continue
        
        # Define output paths
        screenshot_path = os.path.join(
            config.RECORDED_DIR,
            f"screenshot_{i:02d}.{config.SCREENSHOT_FORMAT}"
        )
        audio_path = os.path.join(
            config.RECORDED_DIR,
            f"audio_{i:02d}.{config.AUDIO_FORMAT}"
        )
        
        # Extract screenshot
        if utils.extract_screenshot(video_path, rec_timestamp, screenshot_path):
            print(f"  ✓ Screenshot at {int(rec_timestamp)}s (Ref: {int(ref_timestamp)}s)")
        else:
            print(f"  ✗ Failed to extract screenshot at {int(rec_timestamp)}s")
            continue
        
        # Extract audio clip (adjust duration if near end of video)
        audio_duration = min(config.AUDIO_DURATION, duration - rec_timestamp)
        if utils.extract_audio_clip(video_path, rec_timestamp, audio_duration, audio_path):
            print(f"  ✓ Audio clip at {int(rec_timestamp)}s")
        else:
            print(f"  ✗ Failed to extract audio at {int(rec_timestamp)}s")
            continue
        
        # Add to recorded samples
        recorded_samples.append({
            "index": i,
            "timestamp": rec_timestamp,
            "screenshot": screenshot_path,
            "audio": audio_path
        })
    
    # Update metadata with recorded video info
    metadata["recorded_video"] = video_path
    metadata["recorded_duration"] = duration
    metadata["recorded_samples"] = recorded_samples
    
    return metadata


def load_metadata() -> Dict:
    """Load metadata from JSON file"""
    if not os.path.exists(config.METADATA_FILE):
        raise FileNotFoundError(f"Metadata file not found: {config.METADATA_FILE}")
    
    with open(config.METADATA_FILE, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    # For testing this module independently
    metadata = load_metadata()
    metadata = extract_recorded_data(config.RECORDED_VIDEO, metadata)
    
    # Save updated metadata
    with open(config.METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

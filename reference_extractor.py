"""
Phase 1: Reference Extraction Module
Extracts screenshots and audio clips from the original video at random timestamps
"""

import os
import json
import random
from typing import List, Dict
import config
import utils


def generate_random_timestamps(duration: float, num_samples: int) -> List[float]:
    """
    Generate random timestamps within the video duration
    
    Args:
        duration: Total video duration in seconds
        num_samples: Number of timestamps to generate
        
    Returns:
        List of timestamps in seconds, sorted
    """
    # Define valid range (avoid intro and credits)
    min_time = config.MIN_TIMESTAMP_OFFSET
    max_time = duration - config.MAX_TIMESTAMP_OFFSET
    
    if max_time <= min_time:
        # Video too short, use full range
        min_time = 0
        max_time = duration
    
    # Generate random timestamps
    timestamps = []
    for _ in range(num_samples):
        timestamp = random.uniform(min_time, max_time)
        timestamps.append(round(timestamp, 2))
    
    return sorted(timestamps)


def extract_reference_data(video_path: str) -> Dict:
    """
    Extract reference screenshots and audio clips from original video
    
    Args:
        video_path: Path to the original video
        
    Returns:
        Dictionary containing extraction metadata
    """
    print(f"\n📂 Loading {video_path}...")
    
    # Get video duration
    duration = utils.get_video_duration(video_path)
    if duration is None:
        raise ValueError(f"Failed to get duration for {video_path}")
    
    print(f"   Duration: {utils.format_timestamp(duration)} ({duration:.1f}s)")
    
    # Generate random timestamps
    timestamps = generate_random_timestamps(duration, config.NUM_SAMPLES)
    print(f"🎲 Generated random timestamps: {[int(t) for t in timestamps]}")
    
    # Create output directory
    utils.ensure_directory(config.REFERENCE_DIR)
    
    # Extract screenshots and audio
    print(f"\nPhase 1: Extracting reference data...")
    
    metadata = {
        "original_video": video_path,
        "duration": duration,
        "timestamps": timestamps,
        "audio_duration": config.AUDIO_DURATION,
        "samples": [],
        "anchors": []  # New: Store anchor info
    }
    
    # 1. Extract Random Samples (Fingerprint)
    print("  ► Extracting Random Samples (Fingerprint)...")
    for i, timestamp in enumerate(timestamps):
        # Define output paths
        screenshot_path = os.path.join(
            config.REFERENCE_DIR,
            f"screenshot_{i:02d}.{config.SCREENSHOT_FORMAT}"
        )
        audio_path = os.path.join(
            config.REFERENCE_DIR,
            f"audio_{i:02d}.{config.AUDIO_FORMAT}"
        )
        
        # Extract screenshot
        if utils.extract_screenshot(video_path, timestamp, screenshot_path):
            pass # Suppress log spam
        else:
            print(f"  ✗ Failed to extract screenshot at {int(timestamp)}s")
            continue
        
        # Extract audio clip
        if utils.extract_audio_clip(video_path, timestamp, config.AUDIO_DURATION, audio_path):
            print(f"    ✓ Sample {i}: {int(timestamp)}s")
        else:
            print(f"  ✗ Failed to extract audio at {int(timestamp)}s")
            continue
        
        # Add to metadata
        metadata["samples"].append({
            "index": i,
            "timestamp": timestamp,
            "screenshot": screenshot_path,
            "audio": audio_path
        })

    # 2. Extract Audio Anchors (Sync)
    print("  ► Extracting Audio Anchors (Sync)...")
    
    # Adaptive Anchor Logic
    if duration < 900: # Less than 15 minutes
        print(f"    ℹ Video is short ({int(duration)}s). Using relative anchors (15%, 50%, 85%).")
        anchor_times = [
            int(duration * 0.15),
            int(duration * 0.50),
            int(duration * 0.85)
        ]
    else:
        # Use standard Hackathon anchors
        anchor_times = config.ANCHOR_AUDIO_TIMES

    for i, timestamp in enumerate(anchor_times):
        if timestamp >= duration:
            print(f"    ⚠ Skip anchor {timestamp}s (beyond duration)")
            continue
            
        anchor_path = os.path.join(
            config.REFERENCE_DIR,
            f"anchor_{int(timestamp)}.wav"
        )
        
        # Extract 10s clip
        if utils.extract_audio_clip(video_path, timestamp, config.ANCHOR_DURATION, anchor_path):
            print(f"    ✓ Anchor {i}: {int(timestamp)}s")
            metadata["anchors"].append({
                "timestamp": timestamp,
                "path": anchor_path
            })
        else:
            print(f"    ✗ Failed to extract anchor at {timestamp}s")

    # Save metadata
    with open(config.METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Metadata saved to {config.METADATA_FILE}")
    
    return metadata


if __name__ == "__main__":
    # For testing this module independently
    utils.ensure_directory(config.OUTPUT_DIR)
    extract_reference_data(config.ORIGINAL_VIDEO)

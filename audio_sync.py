"""
Audio Synchronization Module
Finds the time offset between a reference audio track and a recorded video's audio
using Cross-Correlation.
"""

import os
import numpy as np
from scipy import signal
import librosa
import config

def load_audio_segment(path, start_time, duration, sr=8000):
    """
    Load a specific segment of audio at a low sample rate for fast correlation.
    """
    try:
        y, _ = librosa.load(path, sr=sr, offset=start_time, duration=duration)
        return y
    except Exception as e:
        print(f"  ⚠ Error loading audio segment from {path}: {e}")
        return None

def find_offset(ref_path, rec_path, anchor_time, window=60, anchor_duration=10):
    """
    Find the time offset of the recorded video relative to the reference.
    
    Args:
        ref_path: Path to original video/audio
        rec_path: Path to recorded video
        anchor_time: Time in original video to use as anchor
        window: Search window size in seconds (defines search range in recorded video)
        anchor_duration: Duration of the anchor clip
        
    Returns:
        offset (float): deduced *start time* of the recorded video relative to original.
                        e.g., if offset is 10.0, the recorded video starts at 10.0s of original.
                        Returns None if no good match found.
    """
    # 1. Load Anchor from Reference (small clip)
    ref_audio = load_audio_segment(ref_path, anchor_time, anchor_duration)
    if ref_audio is None or len(ref_audio) == 0:
        return None

    # 2. Load Search Region from Recorded (larger clip)
    # We look around the expected time. 
    # If recorded video is roughly synced, anchor should be at 'anchor_time'.
    # We search from [anchor_time - window] to [anchor_time + window].
    # But since recorded video might start LATE (e.g. at 5min mark), we just search 
    # the first few minutes OR a specific window if we have a guess.
    
    # Strategy: For piracy, we often don't know where it starts. 
    # But if we assume the recorded video is a full movie, we search around the anchor time.
    # If it's a clip, we might need a sliding search.
    
    # Simplified Strategy for Hackathon: 
    # Assume recorded video is somewhat linear. We look for the anchor in the recorded video 
    # roughly where it should be, +/- the window.
    
    search_start = max(0, anchor_time - window)
    search_end = anchor_time + window
    search_duration = search_end - search_start
    
    rec_audio = load_audio_segment(rec_path, search_start, search_duration)
    if rec_audio is None or len(rec_audio) < len(ref_audio):
        return None

    # 3. Cross-Correlate
    # Normalize
    ref_audio = (ref_audio - np.mean(ref_audio)) / (np.std(ref_audio) + 1e-6)
    rec_audio = (rec_audio - np.mean(rec_audio)) / (np.std(rec_audio) + 1e-6)
    
    correlation = signal.correlate(rec_audio, ref_audio, mode='valid')
    peak_index = np.argmax(correlation)
    peak_value = correlation[peak_index]
    
    # 4. Calculate Offset
    # peak_index is where the match starts in rec_audio
    # time_in_rec_chunk = peak_index / sr
    sr = 8000
    match_time_in_rec = search_start + (peak_index / sr)
    
    # The moment 'match_time_in_rec' in recorded video corresponds to 'anchor_time' in original.
    # So, Offset = anchor_time - match_time_in_rec
    # Example: Anchor is at 100s. We find it at 10s in recorded video.
    # It means recorded video starts at 90s of original.
    # offset = 100 - 10 = 90.
    
    offset = anchor_time - match_time_in_rec
    
    return offset, peak_value

def get_consensus_offset(ref_path, rec_path, anchors=None):
    """
    Find offset using multiple anchors and take consensus.
    Args:
        anchors: List of dicts [{"timestamp": 300, "path": "..."}] from metadata
    """
    offsets = []
    
    # If no anchors provided, try config (fallback)
    if not anchors:
        print("⚠ No anchors found in metadata. Checking config...")
        target_times = config.ANCHOR_AUDIO_TIMES
    else:
        # We just need the timestamps for logic, but wait..
        # `find_offset` loads the anchor from ref_path using the timestamp.
        # So we just need the timestamps list.
        target_times = [a['timestamp'] for a in anchors]

    print(f"🔄 Syncing Audio (Anchors: {target_times})...")
    
    for anchor_time in target_times:
        result = find_offset(ref_path, rec_path, anchor_time, 
                             window=config.AUDIO_SEARCH_WINDOW,
                             anchor_duration=config.ANCHOR_DURATION)
        
        if result:
            offset, peaks = result
            # Arbitrary threshold for correlation peak - in real world would need tuning
            offsets.append(offset)
            print(f"  - Anchor {anchor_time}s found offset: {offset:.2f}s (Confidence: {peaks:.4f})")
            if peaks < 0.1:
                print("    ⚠ Low confidence! This might be a false match.")
        else:
            print(f"  - Anchor {anchor_time}s not found.")
            
    if not offsets:
        print("❌ No audio sync found. Assuming 0 offset.")
        return 0.0
        
    # Consensus: Median
    final_offset = np.median(offsets)
    print(f"✅ Final Consensus Offset: {final_offset:.2f}s")
    return final_offset

"""
Phase 3: Comparison and Decision Module
Compares extracted data using perceptual hashing and audio similarity
"""

import os
from typing import Dict, Tuple, List
import numpy as np
from PIL import Image
import imagehash
import librosa
import config


def compare_images(img1_path: str, img2_path: str) -> Tuple[bool, int]:
    """
    Compare two images using perceptual hashing with normalization
    
    Args:
        img1_path: Path to first image
        img2_path: Path to second image
        
    Returns:
        Tuple of (is_match, hamming_distance)
    """
    try:
        # Load images
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        # Normalize images for better comparison
        # 1. Resize to consistent dimensions (reduces resolution differences)
        target_size = (512, 512)
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)
        
        # 2. Convert to grayscale (removes color variations)
        img1 = img1.convert('L')
        img2 = img2.convert('L')
        
        # Calculate perceptual hashes
        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(img2)
        
        # Calculate Hamming distance
        distance = hash1 - hash2
        
        # Determine if match
        is_match = distance <= config.IMAGE_HASH_THRESHOLD
        
        return is_match, distance
    except Exception as e:
        print(f"  ⚠ Error comparing images: {e}")
        return False, 999


def compare_audio(audio1_path: str, audio2_path: str) -> Tuple[bool, float]:
    """
    Compare two audio clips using spectrogram-based similarity with normalization
    
    Args:
        audio1_path: Path to first audio file
        audio2_path: Path to second audio file
        
    Returns:
        Tuple of (is_match, similarity_score)
    """
    try:
        # Load audio files
        y1, sr1 = librosa.load(audio1_path, sr=config.AUDIO_SAMPLE_RATE)
        y2, sr2 = librosa.load(audio2_path, sr=config.AUDIO_SAMPLE_RATE)
        
        # Normalize audio amplitude (removes volume differences)
        # RMS normalization: scale to consistent energy level
        def normalize_audio(audio):
            rms = np.sqrt(np.mean(audio**2))
            if rms > 0:
                return audio / rms
            return audio
        
        y1 = normalize_audio(y1)
        y2 = normalize_audio(y2)
        
        # Ensure same length (pad shorter one)
        max_len = max(len(y1), len(y2))
        y1 = np.pad(y1, (0, max_len - len(y1)), mode='constant')
        y2 = np.pad(y2, (0, max_len - len(y2)), mode='constant')
        
        # Generate mel spectrograms
        spec1 = librosa.feature.melspectrogram(y=y1, sr=sr1)
        spec2 = librosa.feature.melspectrogram(y=y2, sr=sr2)
        
        # Flatten spectrograms
        spec1_flat = spec1.flatten()
        spec2_flat = spec2.flatten()
        
        # Ensure same length
        min_len = min(len(spec1_flat), len(spec2_flat))
        spec1_flat = spec1_flat[:min_len]
        spec2_flat = spec2_flat[:min_len]
        
        # Calculate cosine similarity
        dot_product = np.dot(spec1_flat, spec2_flat)
        norm1 = np.linalg.norm(spec1_flat)
        norm2 = np.linalg.norm(spec2_flat)
        
        if norm1 == 0 or norm2 == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (norm1 * norm2)
        
        # Determine if match
        is_match = similarity >= config.AUDIO_SIMILARITY_THRESHOLD
        
        return is_match, similarity
    except Exception as e:
        print(f"  ⚠ Error comparing audio: {e}")
        return False, 0.0


def compare_and_decide(metadata: Dict) -> Dict:
    """
    Compare all extracted data and make piracy decision
    
    Args:
        metadata: Metadata containing all sample information
        
    Returns:
        Dictionary containing comparison results and decision
    """
    print(f"\nPhase 3: Comparing content...")
    
    reference_samples = metadata["samples"]
    recorded_samples = metadata["recorded_samples"]
    
    # Match samples by index
    image_matches = []
    image_distances = []
    audio_similarities = []
    matched_timestamps = []  # List to store timestamps of confirmed matches
    matched_audio_timestamps = [] # List to store timestamps of audio matches
    
    print(f"\n{'='*60}")
    print(f"DETAILED COMPARISON RESULTS")
    print(f"{'='*60}")
    
    for ref_sample in reference_samples:
        # Find corresponding recorded sample
        rec_sample = next(
            (s for s in recorded_samples if s["index"] == ref_sample["index"]),
            None
        )
        
        if rec_sample is None:
            continue
        
        # Compare images
        is_img_match, img_distance = compare_images(
            ref_sample["screenshot"],
            rec_sample["screenshot"]
        )
        image_matches.append(is_img_match)
        image_distances.append(img_distance)
        
        if is_img_match:
            matched_timestamps.append(int(ref_sample['timestamp']))
        
        # Compare audio
        is_audio_match, audio_similarity = compare_audio(
            ref_sample["audio"],
            rec_sample["audio"]
        )
        
        if is_audio_match:
            matched_audio_timestamps.append(int(ref_sample['timestamp']))
        
        audio_similarities.append(audio_similarity)
        
        # Print detailed results for each sample
        print(f"\nSample {ref_sample['index']} @ {int(ref_sample['timestamp'])}s:")
        print(f"  Image Hash Distance: {img_distance} (threshold: {config.IMAGE_HASH_THRESHOLD}) - {'✓ MATCH' if is_img_match else '✗ NO MATCH'}")
        print(f"  Audio Similarity: {audio_similarity:.3f} (threshold: {config.AUDIO_SIMILARITY_THRESHOLD}) - {'✓ MATCH' if is_audio_match else '✗ NO MATCH'}")
    
    print(f"\n{'='*60}")
    
    # Calculate statistics
    total_samples = len(image_matches)
    image_match_count = sum(image_matches)
    image_match_percentage = image_match_count / total_samples if total_samples > 0 else 0
    avg_audio_similarity = np.mean(audio_similarities) if audio_similarities else 0
    avg_image_distance = np.mean(image_distances) if image_distances else 999
    
    # Display results
    print(f"\n🖼️  Visual match: {image_match_count} / {total_samples} ({image_match_percentage*100:.1f}%)")
    print(f"   Average hash distance: {avg_image_distance:.1f}")
    
    audio_level = "HIGH" if avg_audio_similarity >= config.AUDIO_SIMILARITY_THRESHOLD else "LOW"
    print(f"🔊 Audio similarity: {audio_level} (avg: {avg_audio_similarity:.2f})")
    
    
    # Decision logic - optimized for screen-recorded piracy detection
    is_pirated = False
    reason = ""
    
    # Check if we have sufficient visual matches
    visual_match = image_match_percentage >= config.SCREENSHOT_MATCH_PERCENTAGE
    visual_strong = image_match_percentage >= 0.80  # 80%+ is very strong evidence
    
    # Check if audio similarity is reasonable
    # Note: Screen recordings degrade audio significantly, so we're lenient here
    audio_reasonable = avg_audio_similarity >= 0.02  # Very low bar - just checking it's not completely different
    audio_strong = avg_audio_similarity >= config.AUDIO_SIMILARITY_THRESHOLD
    
    # Decision tree optimized for screen-recorded content
    if visual_strong and audio_reasonable:
        # Very strong visual match (80%+) with any audio correlation
        # This is the PRIMARY detection path for screen recordings
        is_pirated = True
        reason = f"Strong visual match: {image_match_percentage*100:.1f}% (threshold: {config.SCREENSHOT_MATCH_PERCENTAGE*100:.1f}%) with audio correlation {avg_audio_similarity:.3f}"
    elif visual_match and audio_strong:
        # Good visual match with strong audio match
        is_pirated = True
        reason = f"Visual {image_match_percentage*100:.1f}% + Strong audio {avg_audio_similarity:.2f}"
    elif visual_match and not config.REQUIRE_AUDIO_CONFIRMATION:
        # Visual only (if audio confirmation not required)
        is_pirated = True
        reason = f"Visual match {image_match_percentage*100:.1f}% >= {config.SCREENSHOT_MATCH_PERCENTAGE*100:.1f}%"
    elif audio_strong and image_match_percentage >= 0.20:
        # High audio similarity with some visual similarity
        is_pirated = True
        reason = f"Audio match {avg_audio_similarity:.2f} >= {config.AUDIO_SIMILARITY_THRESHOLD} with {image_match_percentage*100:.1f}% visual similarity"
    else:
        # Insufficient evidence
        is_pirated = False
        if visual_match and not audio_reasonable:
            reason = f"Visual match {image_match_percentage*100:.1f}% but audio completely different ({avg_audio_similarity:.3f}) - likely false positive"
        else:
            reason = "Neither visual nor audio similarity thresholds met"
    
    # Prepare results
    results = {
        "total_samples": total_samples,
        "image_match_count": image_match_count,
        "image_match_percentage": image_match_percentage,
        "avg_image_distance": avg_image_distance,
        "avg_audio_similarity": avg_audio_similarity,
        "is_pirated": is_pirated,
        "reason": reason,
        "matched_timestamps": matched_timestamps,
        "matched_audio_timestamps": matched_audio_timestamps
    }
    
    return results


if __name__ == "__main__":
    # For testing this module independently
    import json
    with open(config.METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    
    results = compare_and_decide(metadata)
    print(f"\n{'🚨 RESULT: PIRATED' if results['is_pirated'] else '✅ RESULT: NOT PIRATED'}")
    print(f"Reason: {results['reason']}")

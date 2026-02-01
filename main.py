"""
Main Orchestrator for Video Piracy Detection System
Runs all three phases sequentially with demo-friendly output
"""

import os
import sys
import config
import utils
from reference_extractor import extract_reference_data
from recorded_extractor import extract_recorded_data
from comparator import compare_and_decide


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*50)
    print("🎬 Video Piracy Detection System")
    print("="*50)


def print_result(results: dict):
    """Print final result with formatting"""
    print("\n" + "="*50)
    if results["is_pirated"]:
        print("🚨 RESULT: PIRATED")
    else:
        print("✅ RESULT: NOT PIRATED")
    print("="*50)
    print(f"\nReason: {results['reason']}")
    print()


def check_prerequisites():
    """Check if all prerequisites are met"""
    # Check FFmpeg
    if not utils.check_ffmpeg_installed():
        print("❌ Error: FFmpeg is not installed or not in PATH")
        print("   Please install FFmpeg: https://ffmpeg.org/download.html")
        return False
    
    # Check if video files exist
    if not os.path.exists(config.ORIGINAL_VIDEO):
        print(f"❌ Error: Original video not found: {config.ORIGINAL_VIDEO}")
        return False
    
    if not os.path.exists(config.RECORDED_VIDEO):
        print(f"❌ Error: Recorded video not found: {config.RECORDED_VIDEO}")
        return False
    
    return True


def main():
    """Main execution flow"""
    try:
        print_banner()
        
        # Check prerequisites
        if not check_prerequisites():
            sys.exit(1)
        
        # Create output directory
        utils.ensure_directory(config.OUTPUT_DIR)
        
        # Phase 1: Extract reference data from original video
        metadata = extract_reference_data(config.ORIGINAL_VIDEO)
        
        if not metadata["samples"]:
            print("❌ Error: No reference samples were extracted")
            sys.exit(1)
        
        # Phase 2: Extract data from recorded video
        metadata = extract_recorded_data(config.RECORDED_VIDEO, metadata)
        
        if not metadata["recorded_samples"]:
            print("❌ Error: No recorded samples were extracted")
            sys.exit(1)
        
        # Phase 3: Compare and decide
        results = compare_and_decide(metadata)
        
        # Print final result
        print_result(results)
        
        # Optional: Save results to file
        import json
        results_file = os.path.join(config.OUTPUT_DIR, "results.json")
        
        # Convert numpy types to native Python types for JSON serialization
        json_results = {
            "total_samples": int(results["total_samples"]),
            "image_match_count": int(results["image_match_count"]),
            "image_match_percentage": float(results["image_match_percentage"]),
            "avg_image_distance": float(results["avg_image_distance"]),
            "avg_audio_similarity": float(results["avg_audio_similarity"]),
            "is_pirated": bool(results["is_pirated"]),
            "reason": str(results["reason"])
        }
        
        with open(results_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        print(f"📄 Detailed results saved to {results_file}")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

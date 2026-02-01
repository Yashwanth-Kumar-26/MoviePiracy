"""
Utility functions for video and audio processing using FFmpeg
"""

import os
import subprocess
import json
from typing import Optional
import config


def ensure_directory(directory: str) -> None:
    """Create directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)


def get_video_duration(video_path: str) -> Optional[float]:
    """
    Get the duration of a video file in seconds using FFprobe
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Duration in seconds, or None if failed
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        return duration
    except (subprocess.CalledProcessError, KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"❌ Error getting video duration: {e}")
        return None


def extract_screenshot(video_path: str, timestamp: float, output_path: str) -> bool:
    """
    Extract a screenshot from a video at a specific timestamp
    
    Args:
        video_path: Path to the video file
        timestamp: Time in seconds
        output_path: Path to save the screenshot
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = [
            'ffmpeg',
            '-ss', str(timestamp),
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',  # High quality
            '-y',  # Overwrite output file
            output_path
        ]
        
        subprocess.run(
            cmd,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error extracting screenshot at {timestamp}s: {e}")
        return False


def extract_audio_clip(video_path: str, start_time: float, duration: float, output_path: str) -> bool:
    """
    Extract an audio clip from a video
    
    Args:
        video_path: Path to the video file
        start_time: Start time in seconds
        duration: Duration of the clip in seconds
        output_path: Path to save the audio clip
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', video_path,
            '-t', str(duration),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit for WAV
            '-ar', str(config.AUDIO_SAMPLE_RATE),  # Sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite output file
            output_path
        ]
        
        subprocess.run(
            cmd,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error extracting audio at {start_time}s: {e}")
        return False


def format_timestamp(seconds: float) -> str:
    """Format seconds as MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def check_ffmpeg_installed() -> bool:
    """Check if FFmpeg and FFprobe are installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

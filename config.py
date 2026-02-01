import os

# ==================== FILE PATHS ====================
ORIGINAL_VIDEO = "/home/siddu/MyProJects/Competions/CineTry/Hdlal.mp4"
RECORDED_VIDEO = "/home/siddu/MyProJects/Competions/CineTry/dvdlal.mp4"

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REFERENCE_DIR = os.path.join(OUTPUT_DIR, "reference")
RECORDED_DIR = os.path.join(OUTPUT_DIR, "recorded")
METADATA_FILE = os.path.join(OUTPUT_DIR, "metadata.json")

# Demo Directories
OFFLINE_DIR = os.path.join(BASE_DIR, "Offline")
TELEGRAM_DIR = os.path.join(BASE_DIR, "Telegram")
TELEGRAM_DOWNLOADS = os.path.join(BASE_DIR, "Telegram_Downloads")

# ==================== EXTRACTION PARAMETERS ====================
NUM_SAMPLES = 15  # Number of random timestamps to sample
AUDIO_DURATION = 180  # Duration of audio clips for comparison
MIN_TIMESTAMP_OFFSET = 60  # Skip first minute
MAX_TIMESTAMP_OFFSET = 60  # Skip last minute

# ==================== AUDIO SYNC (NEW) ====================
# Anchors for aligning the recorded video with original
ANCHOR_AUDIO_TIMES = [300, 600, 900]  # Take anchors at 5m, 10m, 15m
ANCHOR_DURATION = 10  # 10 second clips for sync
AUDIO_SEARCH_WINDOW = 60  # Look +/- 60 seconds in recorded video

# ==================== COMPARISON THRESHOLDS ====================
IMAGE_HASH_THRESHOLD = 25
AUDIO_SIMILARITY_THRESHOLD = 0.30
SCREENSHOT_MATCH_PERCENTAGE = 0.35
REQUIRE_AUDIO_CONFIRMATION = True

# ==================== MONITORING ====================
USE_EVENT_LISTENER = True  # True=Watchdog, False=Loop
MIN_FILE_SIZE_MB = 10      # Ignore tiny files

# ==================== TELEGRAM (TELETHON) ====================
API_ID = "" # REPLACE WITH YOUR API_ID
API_HASH = ""
SESSION_NAME = ""
TARGET_CHANNELS = [-1003543725909, -1003738573325]  # List of Channel IDs to monitor

# ==================== REPORTING (NEW) ====================
ENABLE_REPORTING = True
# GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/10eJ5dKoMUnaoZNvpkIB8CCY5TaEBn7dcn53ZfjAzPCQ/edit?usp=sharing"
# GOOGLE_CREDENTIALS_FILE = "cineaifest-77f1defe3cd6.json"
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/57e96c9a-26eb-4cc5-8b29-120646c0b9b7"

MOVIE_NAME = "ShathamanamBhavathi"
PRODUCTION_COMPANY = "Dil Raju"
CONTACT_NAME = "Anti-Piracy Team"

# TelReper
TELREPER_PATH = os.path.join(BASE_DIR, "TelReper")  # Assuming it's cloned here

# ==================== FFMPEG PARAMETERS ====================
SCREENSHOT_FORMAT = "png"
AUDIO_FORMAT = "wav"
AUDIO_SAMPLE_RATE = 22050
VERBOSE = True

"""
Telethon Live Bot
Listens to TARGET_CHANNELS, downloads videos, and triggers the detection pipeline.
"""

import sys
import os
import asyncio
from telethon import TelegramClient, events

# Add parent dir to path to import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import recorded_extractor
import comparator
import reporter
import json

# Ensure download dir exists
if not os.path.exists(config.TELEGRAM_DOWNLOADS):
    os.makedirs(config.TELEGRAM_DOWNLOADS)

client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)

def load_metadata():
    if not os.path.exists(config.METADATA_FILE):
        print("❌ Metadata file not found. Run reference_extractor.py first!")
        return None
    with open(config.METADATA_FILE, 'r') as f:
        return json.load(f)

@client.on(events.NewMessage(chats=config.TARGET_CHANNELS))
async def new_video_handler(event):
    if event.message.video or event.message.document:
        # It's a video/file!
        try:
            print(f"\n🎥 New Video detected in {event.chat_id}!")
            
            # 1. Download
            # Format filename: channelID_msgID.ext
            filename = f"{event.chat_id}_{event.id}{event.file.ext}"
            path = os.path.join(config.TELEGRAM_DOWNLOADS, filename)
            
            print(f"⬇ Downloading to {path}...")
            await client.download_media(event.message, path)
            print("✅ Download Complete.")
            
            # 2. Run Detection Pipeline
            # This is synchronous blocking code, might want to offload to thread in real prod
            # but for demo it's fine.
            metadata = load_metadata()
            if not metadata:
                return

            # Extract & Sync
            # We pass the downloaded video path
            updated_info = recorded_extractor.extract_recorded_data(path, metadata)
            
            # Compare
            results = comparator.compare_and_decide(updated_info)
            
            # 3. Report
            if results["is_pirated"]:
                print("🚨 PIRACY DETECTED! Triggering Actions...")
                reporter.handle_detection(results, path)
                # Optional: Reply to message
                # await event.reply("🚨 @Admin Possible Copyright Infringement Detected!")
            else:
                print("✅ Video seems clean.")
                
        except Exception as e:
            print(f"❌ Error handling message: {e}")
            import traceback
            traceback.print_exc()

async def main():
    print(f"🎧 Client Started. Listening to {config.TARGET_CHANNELS}...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Start the async loop
    import asyncio
    asyncio.run(main())

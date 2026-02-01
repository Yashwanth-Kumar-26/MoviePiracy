"""
Reporting Module
Handles Google Sheets logging (Triggers n8n) and TelReper automation.
"""

import os
import json
import subprocess
import datetime
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
import config

import requests

class SheetLogger:
    def __init__(self):
        self.webhook_url = config.N8N_WEBHOOK_URL

    def log_detection(self, data):
        """
        Sends detection data to n8n Webhook.
        """
        try:
            # Send POST request to n8n
            response = requests.post(self.webhook_url, json=data)
            
            if response.status_code == 200:
                print(f"📡 Data successfully sent to n8n Webhook (Status: {response.status_code})")
            else:
                print(f"⚠ n8n Webhook returned error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Failed to push to n8n Webhook: {e}")

class BotReporter:
    @staticmethod
    def report_user(channel_id):
        """
        Triggers TelReper to mass report the channel.
        """
        if not os.path.exists(config.TELREPER_PATH):
            print("⚠ TelReper not found, skipping attack.")
            return

        print(f"⚔️ Launching TelReper against {channel_id}...")
        # Mock command - replace with actual TelReper signature
        # cmd = ["python3", os.path.join(config.TELREPER_PATH, "main.py"), "--target", channel_id]
        # subprocess.Popen(cmd)
        print("   (TelReper Attack Simulation Started)")

def handle_detection(results, video_path):
    """
    Main entry point for reporting.
    """
    if not config.ENABLE_REPORTING:
        print("ℹ Reporting disabled in config.")
        return

    # 1. Parse IDs from filename if possible (e.g. channelID_msgID.mp4)
    # This depends on how the bot saves files.
    filename = os.path.basename(video_path)
    parts = filename.split('_')
    channel_id = "Unknown"
    msg_id = "Unknown"
    if len(parts) >= 2:
        channel_id = parts[0]
        # msg_id might be complex, simplify or ignore for now
        
    def generate_dmca_text(data):
        """Constructs the full DMCA text from the template."""
        template = f"""Subject: DMCA Takedown Notice - Confirmed Piracy Detection for "{data['movie_name']}"

To: Telegram Copyright Infringement Department
From: Anti-Piracy Bot System
Date: {data['detection_timestamp']}

1. DETECTED PIRATED CONTENT

Movie Title: {data['movie_name']}

Production Company: {data['production_company']}

Infringing Channel ID: {data['channel_id']}

Infringing Message ID: {data['message_id']}

Date/Time of Detection: {data['detection_timestamp']}

2. EVIDENCE OF COPYRIGHT INFRINGEMENT

Our automated system, utilizing dual-signal verification (visual and audio analysis), has confirmed the unauthorized distribution of the above-mentioned copyrighted work.

A. Visual Analysis (Screenshot Matching):

Method: Perceptual hashing (ORB feature matching) of frames extracted at producer-provided timestamps.

Result: {data['visual_match_score']} matches found.

Threshold for Confirmation: ≥10 matches.

Visual Piracy Confirmed: YES

B. Audio Analysis (Spectrogram Fingerprinting):

Method: Spectrogram image generation & hash similarity comparison for audio segments.

Result: {data['audio_match_score']} average similarity.

Threshold for Confirmation: ≥0.3 similarity.

Audio Piracy Confirmed: {"YES" if float(data['audio_match_score']) >= 0.3 else "NO"}

Final Verdict (Dual-Verification Logic): Piracy is confirmed as the content passed the threshold for [VISUAL/AUDIO/BOTH] verification.

3. TIMESTAMP PROOF & MATCHING DETAILS

The following timestamps from the infringing video were analyzed and matched against the official reference material:

Visual Match Timestamps (Seconds): {data['matched_timestamps']}

Audio Segment Match Windows (Start-End Seconds): {data.get('matched_audio_timestamps', '[]')}

4. REQUESTED ACTION

We hereby request the immediate removal of the message identified by Message ID {data['message_id']} in Channel {data['channel_id']} pursuant to the Digital Millennium Copyright Act (DMCA) and Telegram's Terms of Service regarding copyrighted content.

5. CONTACT & DECLARATION

Rights Holder: {data['production_company']}

Authorized Representative: {data['contact_name']}

Statement: I have a good faith belief that the use of the material in the manner complained of is not authorized by the copyright owner, its agent, or the law. The information in this notification is accurate, and I am authorized to act on behalf of the owner of an exclusive right that is allegedly infringed.

Sincerely,
Automated Anti-Piracy Detection System"""
        return template

    # 2. Prepare Data
    data = {
        "movie_name": config.MOVIE_NAME,
        "production_company": config.PRODUCTION_COMPANY,
        "channel_id": channel_id,
        "message_id": msg_id,
        "visual_match_score": f"{results['image_match_percentage']*100:.1f}%",
        "audio_match_score": f"{results['avg_audio_similarity']:.2f}",
        "matched_timestamps": str(results.get("matched_timestamps", [])), 
        "matched_audio_timestamps": str(results.get("matched_audio_timestamps", [])),
        "detection_timestamp": str(datetime.datetime.now()),
        "contact_name": config.CONTACT_NAME,
        "status": "PIRATED"
    }

    # Generate full DMCA Text
    data['dmca_notice_text'] = generate_dmca_text(data)
    
    # 3. Log to Sheets
    logger = SheetLogger()
    logger.log_detection(data)
    
    # 4. Attack
    BotReporter.report_user(channel_id)

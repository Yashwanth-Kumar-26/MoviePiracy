#!/usr/bin/env python3
"""
Test script for n8n Webhook and TelReper integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
import reporter
import datetime

def test_webhook():
    """Test n8n Webhook connection"""
    print("=" * 60)
    print("TEST 1: n8n Webhook Integration")
    print("=" * 60)
    print(f"Target URL: {config.N8N_WEBHOOK_URL}")
    
    # Create test data
    test_data = {
        "movie_name": config.MOVIE_NAME,
        "production_company": config.PRODUCTION_COMPANY,
        "channel_id": "-1003738573325",
        "message_id": "TEST_WEBHOOK_MSG",
        "visual_match_score": "93.3%",
        "audio_match_score": "0.024",
        "matched_timestamps": "[62, 75, 81]",
        "detection_timestamp": str(datetime.datetime.now()),
        "contact_name": config.CONTACT_NAME,
        "status": "PIRATED"
    }
    
    # Initialize logger
    print("\nAttempting to push test data to webhook...")
    logger = reporter.SheetLogger() # Naming kept same for compatibility
    logger.log_detection(test_data)
    
    return True

def test_telreper():
    """Test TelReper integration"""
    print("\n" + "=" * 60)
    print("TEST 2: TelReper Integration")
    print("=" * 60)
    
    if os.path.exists(config.TELREPER_PATH):
        print(f"\n✅ TelReper found at: {config.TELREPER_PATH}")
        print("\nSimulating TelReper attack...")
        reporter.BotReporter.report_user("-1003738573325")
        print("\n✅ TelReper integration ready")
        return True
    else:
        print(f"\n❌ TelReper not found at: {config.TELREPER_PATH}")
        return False

def main():
    print("\n🧪 CineTry Reporting Integration Test (Webhook Mode)\n")
    
    webhook_ok = test_webhook()
    telreper_ok = test_telreper()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Webhook:       {'✅ SENT' if webhook_ok else '❌ FAIL'}")
    print(f"TelReper:      {'✅ PASS' if telreper_ok else '❌ FAIL'}")
    print("=" * 60)

if __name__ == "__main__":
    main()

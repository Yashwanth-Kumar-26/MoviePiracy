# CineTry Hackathon Demo Scenario

## Phase 1: Production House Setup (Pre-Demo)
*   **Actor**: You (playing the Studio Tech Lead).
*   **Action**: You run `reference_extractor.py` on the **Original Movie** (`1hd.mkv`).
*   **Result**: The system extracts the "Digital Fingerprint" (Anchors + Hash Data) and saves it to `metadata.json`.
*   **Narrative**: "This is the one-time setup where the Production House secures their content."

## Phase 2: The Judge's Challenge (Offline Demo)
*   **Actor**: The Judge.
*   **Action**: "Okay, show me it works right now on this file."
*   **You**: Run the command: `python Offline/demo.py 1dvd.mp4`.
*   **What Happens**:
    1.  **Audio Sync**: The system finds the exact offset (e.g., "Video is 12s late").
    2.  **Detection**: It compares the fingerprints.
    3.  **Result**: It prints `🚨 PIRATED` on the screen instantly.
    4.  **Proof**: You open **Google Sheets**, and the new row is already there.

## Phase 3: Real-World Protection (Telethon Live Bot)
*   **Actor**: The Pirate (Uploading to Telegram) & The Bot (Listening).
*   **Action**: A Pirate uploads a cam-rip video to the monitored channel (ID: `-1003543725909`).
*   **What Happens (The Automation)**:
    1.  **Instant Detection**: The `Telegram/bot.py` script (running via Telethon) sees the new message immediately.
    2.  **Auto-Download**: It downloads the video to the `Telegram_Downloads/` folder.
    3.  **Alignment & Analysis**:
        *   It finds the **Audio Anchor** (even if the clip starts at 10mins).
        *   It extracts frames and compares them to the Fingerprint.
    4.  **Verdict & Action**:
        *   **Log**: It pushes the Incident Report to **Google Sheets**.
        *   **Notify**: The Sheet triggers **n8n**, which emails the Legal Team.
        *   **Attack**: (Optional) It triggers `TelReper` to report the user.

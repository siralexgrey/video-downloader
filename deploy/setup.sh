#!/bin/bash
set -e

echo "=== Telegram Video Downloader Bot - Server Setup ==="
echo ""

# Install system dependencies
echo "Installing system packages..."
sudo apt update
sudo apt install -y git python3-venv ffmpeg

# Create venv and install Python dependencies
echo "Creating Python virtual environment..."
python3 -m venv .venv

echo "Installing Python packages..."
.venv/bin/pip install -r requirements.txt

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "1. Edit deploy/video-downloader.service and replace TELEGRAM_BOT_TOKEN=REPLACE_ME with your token"
echo "2. Run: sudo cp deploy/video-downloader.service /etc/systemd/system/"
echo "3. Run: sudo systemctl daemon-reload"
echo "4. Run: sudo systemctl enable --now video-downloader"
echo "5. Check logs: sudo journalctl -u video-downloader -f"

# Deployment Guide - Oracle Cloud Always Free

This guide walks you through deploying the Telegram Video Downloader Bot on Oracle Cloud's Always Free ARM VM.

## Prerequisites

- Oracle Cloud account (free tier)
- Telegram bot token from [@BotFather](https://t.me/botfather)
- Git repository with this code (GitHub/GitLab/etc.)

## Step 1: Create Oracle Cloud VM

1. Sign in to [Oracle Cloud Console](https://cloud.oracle.com/)
2. Navigate to: **Compute** → **Instances** → **Create Instance**
3. Configure:
   - **Name**: `telegram-bot` (or any name)
   - **Image**: Ubuntu 24.04
   - **Shape**: Ampere A1 (ARM, Always Free eligible)
   - **Add SSH keys**: Upload your public SSH key or generate new pair
4. Click **Create**
5. Note the **Public IP address** once the instance is running

## Step 2: Connect to the VM

From your local machine:
```bash
ssh -i /path/to/your_private_key ubuntu@<PUBLIC_IP>
```

## Step 3: Clone the Repository

On the VM:
```bash
cd ~
git clone <YOUR_GIT_REPO_URL> video-downloader
cd video-downloader
```

## Step 4: Run Setup Script

```bash
chmod +x deploy/setup.sh
./deploy/setup.sh
```

This installs:
- Python 3 + venv
- ffmpeg (required for video processing)
- Python dependencies

## Step 5: Configure Bot Token

Edit the systemd service file:
```bash
nano deploy/video-downloader.service
```

Replace `TELEGRAM_BOT_TOKEN=REPLACE_ME` with your actual token:
```
Environment=TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

## Step 6: Install and Start the Service

```bash
sudo cp deploy/video-downloader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now video-downloader
```

## Step 7: Check Status

```bash
# Check if running
sudo systemctl status video-downloader

# View live logs
sudo journalctl -u video-downloader -f
```

You should see: `Authorized as @YourBotUsername`

## Your Bot is Live!

Users can now message your bot on Telegram and download videos.

## Useful Commands

```bash
# Restart bot
sudo systemctl restart video-downloader

# Stop bot
sudo systemctl stop video-downloader

# View recent logs
sudo journalctl -u video-downloader -n 50

# Update code from git
cd ~/video-downloader
git pull
sudo systemctl restart video-downloader
```

## Troubleshooting

**Bot not starting?**
- Check logs: `sudo journalctl -u video-downloader -n 50`
- Verify token is correct in `/etc/systemd/system/video-downloader.service`
- Test manually: `cd ~/video-downloader && .venv/bin/python main.py`

**Video downloads failing?**
- Check ffmpeg: `which ffmpeg` (should show `/usr/bin/ffmpeg`)
- Verify disk space: `df -h`
- Check logs for specific errors

**Need to change the token?**
```bash
sudo nano /etc/systemd/system/video-downloader.service
sudo systemctl daemon-reload
sudo systemctl restart video-downloader
```

# Telegram Video Downloader Bot

A Telegram bot that downloads videos from YouTube Shorts, TikTok, Instagram, and X (Twitter).

## Setup

Python 3.10+ is recommended (some dependencies are deprecating Python 3.9).

1. Get your bot token from [@BotFather](https://t.me/botfather).

2. Install dependencies: `pip install -r requirements.txt`

3. Provide the token via environment variable (recommended) or `.env` file.

	 Option A (env var):
	 - `export TELEGRAM_BOT_TOKEN="<your_token_here>"`

	 Option B (local .env file):
	 - Create a file named `.env` in the project root with:
		 - `TELEGRAM_BOT_TOKEN=<your_token_here>`

4. Run: `python main.py`

## Troubleshooting

- `HTTP Error 403: Forbidden` / “Log in required” / private or age-gated content
	- Many platforms (especially Instagram/TikTok/X) will refuse downloads for restricted posts unless you are logged in.
	- This bot is **public-only**. If a link is restricted, the bot will ask the user to open it in their browser.

## Usage

Send a video link to the bot, and it will download and send the video back.

## Deployment

For production deployment on Oracle Cloud Always Free (recommended), see [deploy/DEPLOY.md](deploy/DEPLOY.md).

Quick deployment steps:
1. Create an Oracle Cloud Always Free VM (Ubuntu 24.04, ARM)
2. Clone this repo on the VM
3. Run `./deploy/setup.sh`
4. Configure your token in `deploy/video-downloader.service`
5. Install and start: `sudo cp deploy/video-downloader.service /etc/systemd/system/ && sudo systemctl enable --now video-downloader`

Full instructions with troubleshooting in [deploy/DEPLOY.md](deploy/DEPLOY.md).
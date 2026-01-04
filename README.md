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

**Recommended: Render.com (Free + Easy)**

See [deploy/RENDER_DEPLOY.md](deploy/RENDER_DEPLOY.md) for complete instructions.

Quick steps:
1. Push code to GitHub
2. Create new Web Service on Render.com from your GitHub repo
3. Add `TELEGRAM_BOT_TOKEN` environment variable
4. Deploy (takes 2-5 minutes)
5. Set up free UptimeRobot monitor to keep bot awake 24/7

**Alternative: VPS Deployment**

For self-hosted deployment on Ubuntu/Debian VPS, see [deploy/DEPLOY.md](deploy/DEPLOY.md).

VPS providers:
- Oracle Cloud (Always Free tier)
- DigitalOcean ($4-6/month)
- Hetzner Cloud (€3-5/month)
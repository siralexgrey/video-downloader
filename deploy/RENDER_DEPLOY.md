# Render.com Deployment Guide

Deploy your Telegram bot on Render.com for **free** with 24/7 uptime using a health check cron job.

## Prerequisites

- Render.com account (sign up at https://render.com)
- Telegram bot token from [@BotFather](https://t.me/botfather)
- GitHub repository with this code

## Step 1: Push Code to GitHub

Make sure your code is pushed to GitHub (already done if you're reading this on GitHub).

## Step 2: Deploy on Render

### Option A: One-Click Deploy (Easiest)

1. Go to https://render.com/deploy
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Render will auto-detect settings from `render.yaml`
5. Add environment variable:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Your bot token from BotFather
6. Click **Create Web Service**

### Option B: Manual Setup

1. Go to https://dashboard.render.com/
2. Click **New** → **Web Service**
3. Connect your GitHub account
4. Select your `video-downloader` repository
5. Configure:
   - **Name**: `video-downloader-bot` (or any name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free
6. Add environment variable:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Your bot token
7. Click **Create Web Service**

## Step 3: Wait for Deployment

Render will build and deploy your bot. This takes 2-5 minutes.

Once deployed, you'll see:
- "Your service is live" 
- Logs showing "Authorized as @YourBotName"

**Important**: Render free tier sleeps after 15 minutes of inactivity. We'll fix this in Step 4.

## Step 4: Keep Bot Awake with UptimeRobot

To prevent your bot from sleeping, use a free cron service to ping it every 5-10 minutes.

### Using UptimeRobot (Recommended - Free)

1. Sign up at https://uptimerobot.com/ (free account)
2. Click **Add New Monitor**
3. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: `Telegram Video Bot`
   - **URL**: `https://your-service-name.onrender.com/health`
     (Replace `your-service-name` with your actual Render service name)
   - **Monitoring Interval**: 5 minutes
4. Click **Create Monitor**

### Alternative: cron-job.org

1. Sign up at https://cron-job.org/ (free)
2. Create new cron job
3. **URL**: `https://your-service-name.onrender.com/health`
4. **Schedule**: Every 10 minutes
5. Save

## Step 5: Test Your Bot

1. Open Telegram
2. Find your bot (@YourBotName)
3. Send `/start`
4. Send a video link (YouTube, TikTok, Instagram, X)

The bot should respond immediately!

## Managing Your Deployment

### View Logs
- Go to your Render dashboard
- Click on your service
- Click **Logs** tab

### Update Bot
Push changes to GitHub:
```bash
git add .
git commit -m "Update bot"
git push
```

Render will automatically redeploy (if you enabled auto-deploy).

### Manually Redeploy
- Dashboard → Your Service → **Manual Deploy** → **Deploy latest commit**

### Change Token
- Dashboard → Your Service → **Environment**
- Update `TELEGRAM_BOT_TOKEN` value
- Service will restart automatically

### Monitor Uptime
- Check UptimeRobot dashboard to see uptime percentage
- Should be 99%+ if cron job is working

## Troubleshooting

**Bot not responding?**
- Check Render logs for errors
- Verify token is correct in environment variables
- Ensure UptimeRobot monitor is active (green)

**"Service unavailable" from UptimeRobot?**
- Check if Render service is running (dashboard shows "Live")
- Check logs for startup errors
- Verify health check URL is correct: `https://your-service.onrender.com/health`

**Bot sleeps even with UptimeRobot?**
- Verify monitor interval is 5-10 minutes (not longer)
- Check UptimeRobot monitor status (should be "Up")
- Make sure health check URL includes `/health` path

**Video downloads failing?**
- Check logs for specific yt-dlp errors
- Restricted content will show "open in browser" message to users
- ffmpeg is pre-installed in the Docker container

## Free Tier Limits

Render free tier includes:
- 750 hours/month (enough for 24/7 uptime)
- 512MB RAM
- Automatic HTTPS
- Unlimited bandwidth

With UptimeRobot free tier:
- 50 monitors
- 5-minute check intervals
- Email alerts

## Your Bot is Live! 🎉

Users can now message your bot on Telegram from anywhere and download videos.

The bot will stay awake 24/7 thanks to the health check pings.

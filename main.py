import asyncio
import os
import tempfile
import threading
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError
from http.server import HTTPServer, BaseHTTPRequestHandler

import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


def _is_restricted_availability(value: object) -> bool:
    if not isinstance(value, str):
        return False
    v = value.strip().lower()
    return v in {
        "private",
        "premium_only",
        "subscriber_only",
        "needs_auth",
    }


class _PublicOnlyRestrictedError(RuntimeError):
    pass


def _reply_cant_download_in_bot_text(url: str) -> str:
    return (
        "I can’t download this video in the bot.\n"
        "Open it in your browser instead:\n"
        f"{url}"
    )


def _reply_invalid_url_text() -> str:
    return "Please send a direct link (URL)."


def _reply_generic_failed_text() -> str:
    return "Sorry, I couldn’t download that video. Please try another link."

def _load_token_from_dotenv(dotenv_path: Path) -> Optional[str]:
    if not dotenv_path.exists():
        return None

    try:
        for raw_line in dotenv_path.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            if key.strip() != 'TELEGRAM_BOT_TOKEN':
                continue
            token = value.strip().strip('"').strip("'")
            return token or None
    except OSError:
        return None

    return None


def get_bot_token() -> str:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token:
        return token

    token = _load_token_from_dotenv(Path(__file__).with_name('.env'))
    if token:
        return token

    raise RuntimeError(
        'Missing TELEGRAM_BOT_TOKEN. Set it in your environment or create a .env file with TELEGRAM_BOT_TOKEN=...'
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text('Send me a video link from YouTube, TikTok, Instagram, or Twitter!')

async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    text = (update.message.text or '').strip()
    url = text.split()[0] if text else ''
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text(_reply_invalid_url_text())
        return

    def _download_video(download_url: str, download_dir: str) -> Path:
        outtmpl = str(Path(download_dir) / '%(title).200B-%(id)s.%(ext)s')

        ydl_opts = {
            'outtmpl': outtmpl,
            'noplaylist': True,
            'format': 'best[height<=720]/best',
            'quiet': True,
            'no_warnings': True,
            'retries': 3,
            'fragment_retries': 3,
            'socket_timeout': 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(download_url, download=False)
            if _is_restricted_availability(info.get('availability')):
                raise _PublicOnlyRestrictedError()
            info = ydl.process_ie_result(info, download=True)
            return Path(ydl.prepare_filename(info))

    try:
        with tempfile.TemporaryDirectory(prefix='tg_video_') as temp_dir:
            video_path = await asyncio.to_thread(_download_video, url, temp_dir)
            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(video_file)
    except yt_dlp.utils.DownloadError as e:
        message = str(e).lower()
        if 'http error 403' in message or ' 403' in message or '403:' in message:
            await update.message.reply_text(_reply_cant_download_in_bot_text(url))
        else:
            await update.message.reply_text(_reply_generic_failed_text())
    except _PublicOnlyRestrictedError:
        await update.message.reply_text(_reply_cant_download_in_bot_text(url))
    except HTTPError as e:
        if e.code == 403:
            await update.message.reply_text(_reply_cant_download_in_bot_text(url))
        else:
            await update.message.reply_text(_reply_generic_failed_text())
    except Exception as e:
        await update.message.reply_text(_reply_generic_failed_text())

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

def start_health_check_server(port: int = 8080):
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Health check server running on port {port}")

def main() -> None:
    async def _post_init(app: Application) -> None:
        me = await app.bot.get_me()
        print(f"Authorized as @{me.username}")

    # Start health check server for platforms like Render
    port = int(os.getenv('PORT', '8080'))
    start_health_check_server(port)

    token = get_bot_token()
    application = Application.builder().token(token).post_init(_post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send))
    
    application.run_polling()

if __name__ == '__main__':
    main()
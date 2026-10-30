import os
import asyncio
import tempfile
from pathlib import Path

import yt_dlp
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n"
        "Instagram video havolasini yuboring. 🎬"
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com/" not in url:
        await update.message.reply_text("❌ Instagram havolasini yuboring!")
        return

    msg = await update.message.reply_text("⏳ Video yuklanmoqda...")

    try:
        with tempfile.TemporaryDirectory() as folder:
            options = {
                "outtmpl": f"{folder}/video.%(ext)s",
                "format": "best[ext=mp4]/best",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
            }

            loop = asyncio.get_running_loop()

            def download():
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])

            await loop.run_in_executor(None, download)

            files = list(Path(folder).glob("video.*"))

            if not files:
                raise Exception("Video topilmadi")

            video = files[0]

            with open(video, "rb") as f:
                await update.message.reply_video(
                    video=f,
                    caption="✅ Video tayyor!"
                )

        await msg.delete()

    except Exception:
        await msg.edit_text(
            "❌ Videoni yuklab bo'lmadi. "
            "Havolani tekshirib qayta yuboring."
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
    )

    print("Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()

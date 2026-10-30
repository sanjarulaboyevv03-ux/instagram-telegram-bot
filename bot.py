import os
import asyncio
import tempfile
from pathlib import Path

import yt_dlp

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    "@Qora_ritsar_uz",
    "@ENGZORMUZIKALARR"
]

INSTAGRAM = "https://www.instagram.com/sanjarulaboyevvv/"


def buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 1-kanalga obuna bo‘lish",
                url="https://t.me/Qora_ritsar_uz"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 2-kanalga obuna bo‘lish",
                url="https://t.me/ENGZORMUZIKALARR"
            )
        ],
        [
            InlineKeyboardButton(
                "📸 Instagram sahifamiz",
                url=INSTAGRAM
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Obunani tekshirish",
                callback_data="check"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def check_sub(user_id, bot):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(
                channel,
                user_id
            )

            if member.status in ["left", "kicked"]:
                return False

        except Exception:
            return False

    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "🎬 Instagram video yuklovchi botga xush kelibsiz!\n\n"
        "Botdan foydalanish uchun uchta kanalga ham obuna bo‘ling.\n\n"
        "Obuna bo‘lgach, tekshirish tugmasini bosing.",
        reply_markup=buttons()
    )


async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if await check_sub(query.from_user.id, context.bot):
        await query.answer("✅ Obuna tasdiqlandi!")

        await query.message.reply_text(
            "🎉 Tabriklaymiz!\n\n"
            "Endi Instagram video havolasini yuborishingiz mumkin."
        )

    else:
        await query.answer(
            "❌ Ikkala kanalga ham obuna bo‘ling!",
            show_alert=True
        )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_sub(
        update.effective_user.id,
        context.bot
    ):
        await update.message.reply_text(
            "❌ Avval ikkala kanalga obuna bo‘ling!",
            reply_markup=buttons()
        )
        return

    url = update.message.text.strip()

    if "instagram.com/" not in url:
        await update.message.reply_text(
            "❌ Instagram havolasini yuboring!"
        )
        return

    msg = await update.message.reply_text(
        "⏳ Video yuklanmoqda, kuting..."
    )

    try:
        with tempfile.TemporaryDirectory() as folder:

            options = {
                "outtmpl": f"{folder}/video.%(ext)s",
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "noplaylist": True,
                "max_filesize": 49 * 1024 * 1024
            }

            def download():
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])

            await asyncio.to_thread(download)

            files = list(Path(folder).glob("video.*"))

            if not files:
                raise Exception("Video topilmadi")

            await msg.delete()

            with open(files[0], "rb") as video:
                await update.message.reply_video(
                    video=video,
                    caption="✅ Video tayyor!\n\n"
                            "📸 Instagram: @sanjarulaboyevvv"
                )

    except Exception:
        await msg.edit_text(
            "❌ Videoni yuklab bo‘lmadi.\n\n"
            "Boshqa Instagram havolasini sinab ko‘ring."
        )


def main():

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            check_button,
            pattern="^check$"
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_video
        )
    )

    print("BOT ISHLADI!")

    app.run_polling()


if __name__ == "__main__":
    main()

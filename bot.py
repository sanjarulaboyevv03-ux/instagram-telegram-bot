
import os
import asyncio
import tempfile
import json
from pathlib import Path

import yt_dlp

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
    MenuButtonWebApp,
    WebAppInfo
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)


# ==================================
# SOZLAMALAR
# ==================================

TOKEN = os.getenv("BOT_TOKEN")

WEBAPP_URL = (
    "https://sanjarulaboyevv03-ux.github.io/"
    "instagram-telegram-bot/"
)

ADMIN_ID = 5483351113

CHANNELS = [
    "@Qora_ritsar_uz",
    "@ENGZORMUZIKALARR"
]

INSTAGRAM = "https://www.instagram.com/sanjarulaboyevvv/"


# ==================================
# OBUNA TUGMALARI
# ==================================

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
                "📸 Instagram",
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


# ==================================
# ASOSIY MENYU
# ==================================

def main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Mini Appni ochish",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                "📥 Video yuklash",
                callback_data="download"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Kanallarimiz",
                callback_data="channels"
            )
        ],
        [
            InlineKeyboardButton(
                "📸 Instagram",
                url=INSTAGRAM
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ Bot haqida",
                callback_data="about"
            ),
            InlineKeyboardButton(
                "🆘 Yordam",
                callback_data="help"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# ==================================
# OBUNANI TEKSHIRISH
# ==================================

async def check_sub(user_id, bot):

    for channel in CHANNELS:

        try:
            member = await bot.get_chat_member(
                channel,
                user_id
            )

            if member.status in ["left", "kicked"]:
                return False

        except Exception as error:
            print("Obuna tekshirish xatosi:", error)
            return False

    return True


# ==================================
# VIDEO YUKLASH FUNKSIYASI
# ==================================

async def download_instagram(update, url):

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
                    caption=(
                        "✅ Video tayyor!\n\n"
                        "📸 Instagram: @sanjarulaboyevvv"
                    )
                )

    except Exception as error:

        print("Video yuklash xatosi:", error)

        await msg.edit_text(
            "❌ Videoni yuklab bo‘lmadi.\n\n"
            "Boshqa Instagram havolasini sinab ko‘ring."
        )


# ==================================
# START
# ==================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if await check_sub(user_id, context.bot):

        await update.message.reply_text(
            "👋 Assalomu alaykum!\n\n"
            "🎬 Instagram video yuklovchi botga xush kelibsiz!\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu()
        )

    else:

        await update.message.reply_text(
            "👋 Assalomu alaykum!\n\n"
            "Botdan foydalanish uchun ikkala kanalga obuna bo‘ling.",
            reply_markup=buttons()
        )


# ==================================
# OBUNANI TEKSHIRISH TUGMASI
# ==================================

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if await check_sub(query.from_user.id, context.bot):

        await query.message.reply_text(
            "🎉 Tabriklaymiz!\n\n"
            "Obuna tasdiqlandi.\n\n"
            "Asosiy menyu:",
            reply_markup=main_menu()
        )

    else:

        await query.answer(
            "❌ Ikkala kanalga ham obuna bo‘ling!",
            show_alert=True
        )


# ==================================
# MENYU TUGMALARI
# ==================================

async def menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if not await check_sub(query.from_user.id, context.bot):

        await query.message.reply_text(
            "❌ Avval kanallarga obuna bo‘ling!",
            reply_markup=buttons()
        )

        return

    if query.data == "download":

        await query.message.reply_text(
            "📥 Instagram video havolasini yuboring."
        )

    elif query.data == "channels":

        await query.message.reply_text(
            "📢 Bizning kanallarimiz:",
            reply_markup=buttons()
        )

    elif query.data == "about":

        await query.message.reply_text(
            "ℹ️ BOT HAQIDA\n\n"
            "🎬 Instagram video yuklovchi bot.\n"
            "⚡ Tez va qulay.\n\n"
            "👤 Admin: @sanjarulaboyevvv"
        )

    elif query.data == "help":

        await query.message.reply_text(
            "🆘 YORDAM\n\n"
            "1. Instagramga kiring.\n"
            "2. Video havolasini nusxalang.\n"
            "3. Botga yuboring.\n"
            "4. Video tayyor bo‘ladi."
        )


# ==================================
# MINI APP ORQALI KELGAN MA'LUMOT
# ==================================

async def web_app_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not await check_sub(user_id, context.bot):

        await update.message.reply_text(
            "❌ Avval ikkala kanalga obuna bo‘ling!",
            reply_markup=buttons()
        )

        return

    try:

        data = json.loads(update.effective_message.web_app_data.data)

        action = data.get("action")

        if action == "download":

            url = data.get("url", "").strip()

            if "instagram.com/" not in url:

                await update.message.reply_text(
                    "❌ Instagram havolasini yuboring!"
                )

                return

            await download_instagram(update, url)

        elif action == "admin_stats":

            if user_id != ADMIN_ID:
                await update.message.reply_text(
                    "❌ Sizda admin huquqi yo‘q."
                )
                return

            await update.message.reply_text(
                "👑 Admin panel so‘rovi qabul qilindi."
            )

        else:

            await update.message.reply_text(
                "❌ Noma’lum amal."
            )

    except Exception as error:

        print("Mini App xatosi:", error)

        await update.message.reply_text(
            "❌ Mini App ma’lumotini o‘qishda xatolik."
        )


# ==================================
# ODDIY XABARDAN VIDEO YUKLASH
# ==================================

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_sub(update.effective_user.id, context.bot):

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

    await download_instagram(update, url)


# ==================================
# YORDAM
# ==================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🆘 YORDAM\n\n"
        "Instagram video havolasini botga yuboring.\n\n"
        "👤 Admin: @sanjarulaboyevvv"
    )


# ==================================
# BOT HAQIDA
# ==================================

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎬 Instagram Video Downloader\n\n"
        "⚡ Tez va qulay.\n"
        "👤 Admin: @sanjarulaboyevvv"
    )


# ==================================
# TELEGRAM MINI APP TUGMASI
# ==================================

async def post_init(app):

    await app.bot.set_my_commands([
        BotCommand("start", "🏠 Bosh menyu"),
        BotCommand("help", "🆘 Yordam"),
        BotCommand("about", "ℹ️ Bot haqida")
    ])

    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="🚀 Mini App",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )


# ==================================
# BOTNI ISHGA TUSHIRISH
# ==================================

def main():

    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN topilmadi! GitHub Secrets sozlamasini tekshiring."
        )

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("about", about_command)
    )

    app.add_handler(
        CallbackQueryHandler(
            check_button,
            pattern="^check$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            menu_buttons,
            pattern="^(download|channels|about|help)$"
        )
    )

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.WEB_APP_DATA,
            web_app_handler
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
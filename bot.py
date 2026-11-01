import os
import asyncio
import tempfile
import json
from pathlib import Path
from urllib.parse import urlparse

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


# ==============================
# SOZLAMALAR
# ==============================

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


# ==============================
# OBUNA TUGMALARI
# ==============================

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


# ==============================
# ASOSIY MENYU
# ==============================

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


# ==============================
# OBUNANI TEKSHIRISH
# ==============================

async def check_sub(user_id, bot):

    for channel in CHANNELS:

        try:

            member = await bot.get_chat_member(
                channel,
                user_id
            )

            if member.status in

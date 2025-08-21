# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re
import asyncio
from config import *
from lazydeveloper.helpers import validate_query
from telethon import TelegramClient
from telethon.sessions import StringSession
from lazydeveloper.lazydb import db
from fuzzywuzzy import process

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

# Store user search data for pagination
user_search_data = {}

# Fuzzy filter function
def fuzzy_filter(query, choices, limit=20):
    results = process.extract(query, [c[0] for c in choices], limit=limit)
    matched = []
    for title, score in results:
        if score >= 50:  # minimum matching score
            for c in choices:
                if c[0] == title:
                    matched.append(c)
    return matched

@Client.on_message(filters.group & filters.text & filters.incoming & ~filters.command(['start']))
async def message_handler(client, message):
    try:
        if message.text.startswith("/"):
            return

        args = message.text
        txt = await message.reply(f"**⏳ Searching for links matching:** `{args}` 🔍")

        queryz = await validate_query(args)
        if not queryz:
            await message.reply("Please provide a valid search query.")
            return

        await asyncio.sleep(1)
        sessionstring = await db.get_session(OWNER_ID)
        if sessionstring is None:
            await txt.delete()
            return await message.reply(
                "Please visit again later. I’m waiting for my owner to initialize me. 😔\n\n"
                "If you know my owner, kindly ask him to initialize me. ❤️"
            )

        Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)

        if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()

        search_results = []
        try:
            async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=50):
                if search_msg.text:
                    match = re.match(r"(https?://[^\s]+)", search_msg.text)
                    if match:
                        target_url = match.group(1).strip()
                        movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                        movie_name = movie_name_match.group(1).strip() if movie_name_match else "Unknown Title"
                        search_results.append((movie_name, target_url))
        except Exception as e:
            print(f"Error while searching messages: {e}")
            await message.reply("An error occurred while searching.")
            return

        # Apply fuzzy filter
        filtered_results = fuzzy_filter(queryz, search_results)

        if not filtered_results:
            no_result_text = (
                f"**No results found for '{queryz}'**\n\n"
                f"Try refining your query or checking spelling on "
                f"[Google](http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie) 🔍."
            )
            await txt.delete()
            await message.reply(no_result_text, disable_web_page_preview=True)
            return

        # Save user data for pagination
        user_search_data[message.from_user.id] = {
            "query": queryz,
            "results": filtered_results,
            "page": 0
        }

        await send_paginated_results(message, filtered_results, 0, txt)

        await Lazyuserbot.disconnect()

    except Exception as e:
        print(e)
        if txt:
            await txt.delete()
        await message.reply("I couldn't process your request. Please try again later.")

# Function to send paginated results
async def send_paginated_results(message, results, page, txt=None, query=None):
    start = page * 3
    end = start + 3
    current_results = results[start:end]

    result_message = "\n".join([
        f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {url}</blockquote>"
        for movie_name, url in current_results
    ])

    response = (
        f"**🤞Search Results (Page {page+1}) for '{user_search_data[message.from_user.id]['query']}':**\n\n"
        f"{result_message}\n\n"
    )

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"back_{page-1}"))
    if end < len(results):
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"next_{page+1}"))

    reply_button = InlineKeyboardMarkup([
        nav_buttons,
        [
            InlineKeyboardButton("How To Open Link ❓", url="https://t.me/FilmyflyLinkOpen")
        ],
        [
            InlineKeyboardButton("🪅Request", url="https://t.me/+Aa-zL92bgqQ4OTll"),
            InlineKeyboardButton("♻️Backup", url="https://t.me/AllTypeOfLinkss")
        ],
        [
            InlineKeyboardButton("18+ Channel 🔞", url="https://t.me/+IdabhmoGn1VlNWJl")
        ]
    ])

    if query:
        await query.edit_message_text(response, reply_markup=reply_button, disable_web_page_preview=True)
    else:
        if txt:
            await txt.delete()
        await message.reply(response, reply_markup=reply_button, disable_web_page_preview=True)

# Callback for pagination buttons
@Client.on_callback_query()
async def callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in user_search_data:
        await callback_query.answer("Session expired. Please search again.")
        return

    results = user_search_data[user_id]["results"]

    if callback_query.data.startswith("next_"):
        page = int(callback_query.data.split("_")[1])
    elif callback_query.data.startswith("back_"):
        page = int(callback_query.data.split("_")[1])
    else:
        return

    user_search_data[user_id]["page"] = page
    await send_paginated_results(callback_query.message, results, page, query=callback_query)

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telethon import TelegramClient
from telethon.sessions import StringSession
from lazydeveloper.lazydb import db
import re
import asyncio
from config import *
from lazydeveloper.helpers import validate_query

# ====================== 💘❤👩‍💻==================================== 
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

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
            async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=5):
                if search_msg.text:
                    match = re.match(r"(https?://[^\s]+)", search_msg.text)
                    if match:
                        target_url = match.group(1).strip()
                        # Extract title from round brackets
                        movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                        movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
                        search_results.append((movie_name, target_url))
        except Exception as e:
            print(f"Error while searching messages: {e}")
            await message.reply("An error occurred while searching.")
            return

        if not search_results:
            no_result_text = (
                f"**No results found for '{queryz}'**\n\n"
                f"Try refining your query or checking spelling on "
                f"[Google](http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie) 🔍."
            )
            await txt.delete()
            await message.reply(no_result_text, disable_web_page_preview=True)
            return

        result_message = "\n".join(
            [f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {target_url}</blockquote>"
             for movie_name, target_url in search_results]
        )

        response = (
            f"**🤞Search Results for '{queryz}':**\n\n"
            f"{result_message}\n\n"
        )

        show_pagination = len(search_results) >= 5
        buttons = []

        if show_pagination:
            buttons.append([
                InlineKeyboardButton(f"⬅️ Back", callback_data=f"back|{queryz}|0"),
                InlineKeyboardButton(f"Next ➡️", callback_data=f"next|{queryz}|0")
            ])

        buttons.extend([
            [InlineKeyboardButton(f"How To Open Link ❓", url="https://t.me/FilmyflyLinkOpen")],
            [
                InlineKeyboardButton(f"🪅Request", url="https://t.me/+Aa-zL92bgqQ4OTll"),
                InlineKeyboardButton(f"♻️Backup", url="https://t.me/AllTypeOfLinkss")
            ],
            [InlineKeyboardButton(f"18+  Channel 🔞", url="https://t.me/+IdabhmoGn1VlNWJl")]
        ])

        reply_button = InlineKeyboardMarkup(buttons)

        await txt.delete()
        await message.reply(response, reply_markup=reply_button, disable_web_page_preview=True)

    except Exception as e:
        print(e)
        if txt:
            await txt.delete()
        await message.reply("I couldn't process your request. Please try again later.")

    finally:
        await asyncio.sleep(2)
        await Lazyuserbot.disconnect()


# =================== CALLBACK QUERY HANDLER FOR PAGINATION ===================
@Client.on_callback_query()
async def callback_query_handler(client: Client, callback_query: CallbackQuery):
    try:
        data_parts = callback_query.data.split("|")
        if len(data_parts) < 3:
            return

        action = data_parts[0]
        queryz = data_parts[1]
        page = int(data_parts[2])

        if action == "next":
            page += 1
        elif action == "back":
            page = max(0, page - 1)

        sessionstring = await db.get_session(OWNER_ID)
        if sessionstring is None:
            await callback_query.answer("Bot is not initialized.", show_alert=True)
            return

        Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
        if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()

        search_results = []
        async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=5, offset=page * 5):
            if search_msg.text:
                match_url = re.match(r"(https?://[^\s]+)", search_msg.text)
                if match_url:
                    target_url = match_url.group(1).strip()
                    movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                    movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
                    search_results.append((movie_name, target_url))

        if not search_results:
            await callback_query.answer("No more results.", show_alert=True)
            await Lazyuserbot.disconnect()
            return

        result_message = "\n".join(
            [f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {target_url}</blockquote>"
             for movie_name, target_url in search_results]
        )

        response = (
            f"**🤞Search Results for '{queryz}':**\n\n"
            f"{result_message}\n\n"
        )

        show_pagination = len(search_results) >= 5
        buttons = []

        if show_pagination:
            buttons.append([
                InlineKeyboardButton(f"⬅️ Back", callback_data=f"back|{queryz}|{page}"),
                InlineKeyboardButton(f"Next ➡️", callback_data=f"next|{queryz}|{page}")
            ])

        buttons.extend([
            [InlineKeyboardButton(f"How To Open Link ❓", url="https://t.me/FilmyflyLinkOpen")],
            [
                InlineKeyboardButton(f"🪅Request", url="https://t.me/+Aa-zL92bgqQ4OTll"),
                InlineKeyboardButton(f"♻️Backup", url="https://t.me/AllTypeOfLinkss")
            ],
            [InlineKeyboardButton(f"18+  Channel 🔞", url="https://t.me/+IdabhmoGn1VlNWJl")]
        ])

        reply_button = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit(response, reply_markup=reply_button, disable_web_page_preview=True)

    except Exception as e:
        print(f"Error in callback: {e}")
    finally:
        await Lazyuserbot.disconnect()

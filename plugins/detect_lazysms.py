# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters, enums
# from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from pyrogram import Client, filters
import re
import asyncio
from config import *
from lazydeveloper.helpers import  validate_query
# Initialize Pyrogram Client
from telethon import TelegramClient
from telethon.sessions import StringSession
from lazydeveloper.lazydb import db


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_message(filters.group & filters.text & filters.incoming & ~filters.command(['start']))
async def message_handler(client, message):
      try:
         if message.text.startswith("/"):
               return

         print("\nMessage Received: " + message.text)

        # Validate and sanitize query
         args = message.text
         txt = await message.reply(f"**⏳ Searching for links matching:** `{args}` 🔍")
         
         queryz = await validate_query(args)
         if not queryz:
               await message.reply("Please provide a valid search query.")
               return
         
         # print(f"Search Query: {queryz}")

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
         await asyncio.sleep(1)
         sessionstring = await db.get_session(OWNER_ID)
         if sessionstring is None:
            await txt.delete()
            # msstt h na - 😂 - isiliye copy krne aaye ho 😂 - kr lo - kr lo 
            return await message.reply(
               "Please visit again later. I’m waiting for my owner to initialize me. 😔\n\n"
               "If you know my owner, kindly ask him to initialize me. ❤️"
            )
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

         Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
         
         if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()
         # await Lazyuserbot.start()

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

#================================================================================================================ 
#================================================================================================================ 
      #   Start search logic 1️⃣ // Hey this is LazyDeveloper, & I am writing this for developers ! 
#================================================================================================================ 
      #   This is advance search method for searching url in any message
#================================================================================================================ 
#================================================================================================================ 
         # search_results = []
         # try:
         #    # Search for messages containing the query term in the database channel
         #    async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=5):
         #       if search_msg.text:
         #             # Look for a URL in the first line
         #          match = re.match(r"(https?://[^\s]+)", search_msg.text)
         #          if match:
         #             search_results.append(match.group(1))  # Append the URL
         # except Exception as e:
         #       print(f"Error while searching messages: {e}")
         #       await message.reply("An error occurred while searching.")
         #       return

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

#================================================================================================================ 
#================================================================================================================ 
      #   Start search logic 2️⃣ // Hey this is LazyDeveloper, & I am writing this for developers ! 
#================================================================================================================
#================================================================================================================ 

         search_results = []
         try:
            # Search for messages containing the query term in the database channel
            async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=5):
               if search_msg.text:
                     # Look for a URL in the first line
                     match = re.match(r"(https?://[^\s]+)", search_msg.text)
                     if match:
                        target_url = match.group(1).strip()  # Extract the URL
                        
                        # Extract the movie name from text in parentheses ()
                        movie_name_match = re.search(r"([^)]+)", search_msg.text)
                        movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
                        
                        # Append the result as a tuple of (movie_name, target_url)
                        search_results.append((movie_name, target_url))
         except Exception as e:
            print(f"Error while searching messages: {e}")
            await message.reply("An error occurred while searching.")
            return
 
        # Handle no results
         if not search_results:
            no_result_text = (
                f"**No results found for '{queryz}'**\n\n"
                f"Try refining your query or checking spelling on "
                f"[Google](http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie) 🔍."
            )
            await txt.delete()
            await message.reply(no_result_text, disable_web_page_preview=True)
            return

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

         result_message = "\n".join([f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {target_url}</blockquote>" for movie_name, target_url in search_results])
         print('got result')
         response = (
            f"**🤞Search Results for '{queryz}':**\n\n"
            f"{result_message}\n\n"
         )

         # Pagination button show only if results >= 5
         show_pagination = len(search_results) >= 5

         buttons = []
         if show_pagination:
             buttons.append([
                 InlineKeyboardButton(f"⬅️ Back", callback_data="back"),
                 InlineKeyboardButton(f"Next ➡️", callback_data="next")
             ])

         buttons.extend([
             [InlineKeyboardButton(f"How To Open Link ❓", url=f"https://t.me/FilmyflyLinkOpen")],
             [
                 InlineKeyboardButton(f"🪅Request", url=f"https://t.me/+Aa-zL92bgqQ4OTll"),
                 InlineKeyboardButton(f"♻️Backup", url=f"https://t.me/AllTypeOfLinkss")
             ],
             [InlineKeyboardButton(f"18+  Channel 🔞", url=f"https://t.me/+IdabhmoGn1VlNWJl")]
         ])

         reply_button = InlineKeyboardMarkup(buttons)
         
         await txt.delete()
         result = await message.reply(response, reply_markup=reply_button, disable_web_page_preview=True)

         # Auto-delete results after a delay
         await asyncio.sleep(AUTO_DELETE_TIME)
         await result.delete()

      except Exception as e:
         print(e)
         if txt:
               await txt.delete()
         await message.reply("I couldn't process your request. Please try again later.")
      finally:
         await asyncio.sleep(2)
         # tried to avoid overhead  - session load !
         await Lazyuserbot.disconnect()
         if not Lazyuserbot.is_connected():
               print("Session is disconnected successfully!")
         else:
               print("Session is still connected.")
               await Lazyuserbot.disconnect()
               print("⚠ Tried to disconnect session.\n If u r seeing this message again again then please report to  @LazyDeveloper ❤")
         return


# =================== CALLBACK QUERY HANDLER FOR PAGINATION ===================

@Client.on_callback_query()
async def callback_query_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data

    if data not in ["back", "next"]:
        return

    message = callback_query.message
    if not message or not message.reply_to_message:
        await callback_query.answer("Invalid operation.", show_alert=True)
        return

    original_query = message.reply_to_message.text or ""
    import re
    match = re.search(r"⏳ Searching for links matching: `(.*?)` 🔍", original_query)
    if not match:
        await callback_query.answer("Sorry, can't find the original query.", show_alert=True)
        return

    queryz = match.group(1)

    # In-memory pagination state
    if not hasattr(client, "_pagination_state"):
        client._pagination_state = {}

    user_id = callback_query.from_user.id
    key = f"{user_id}:{queryz}"

    current_page = client._pagination_state.get(key, 0)

    if data == "next":
        current_page += 1
    elif data == "back":
        current_page -= 1
        if current_page < 0:
            current_page = 0

    client._pagination_state[key] = current_page

    sessionstring = await db.get_session(OWNER_ID)
    if sessionstring is None:
        await callback_query.answer("Bot is not initialized.", show_alert=True)
        return

    Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
    if not Lazyuserbot.is_connected():
        await Lazyuserbot.start()

    search_results = []
    try:
        async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=5, offset=current_page*5):
            if search_msg.text:
                match_url = re.match(r"(https?://[^\s]+)", search_msg.text)
                if match_url:
                    target_url = match_url.group(1).strip()
                    movie_name_match = re.search(r"([^)]+)", search_msg.text)
                    movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
                    search_results.append((movie_name, target_url))
    except Exception as e:
        print(f"Error while paginating messages: {e}")
        await callback_query.answer("An error occurred while searching.", show_alert=True)
        await Lazyuserbot.disconnect()
        return

    if not search_results:
        if data == "next":
            current_page -= 1
            if current_page < 0:
                current_page = 0
            client._pagination_state[key] = current_page
        await callback_query.answer("No more results.", show_alert=True)
        await Lazyuserbot.disconnect()
        return

    result_message = "\n".join(
        [f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {target_url}</blockquote>" for movie_name, target_url in search_results]
    )
    response = (
        f"**🤞Search Results for '{queryz}':**\n\n"
        f"{result_message}\n\n"
    )

    show_pagination = len(search_results) >= 5

    buttons = []
    if show_pagination:
        buttons.append([
            InlineKeyboardButton(f"⬅️ Back", callback_data="back"),
            InlineKeyboardButton(f"Next ➡️", callback_data="next")
        ])

    buttons.extend([
        [InlineKeyboardButton(f"How To Open Link ❓", url=f"https://t.me/FilmyflyLinkOpen")],
        [
            InlineKeyboardButton(f"

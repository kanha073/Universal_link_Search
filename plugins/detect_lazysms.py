
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters, enums
# from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
      #   in you database channel, Ex; If any message contains the movie name 
      #   searched by user in db channel , and if that message has any link, then 
      #   bot will only extract the link from the messages 
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
      #   This is super advance search method for searching url + Name in any message                            |🧧 CONTACT ME @LAZYDEVELOPERR
      #   in you database channel, Ex; If any message contains the movie name                                    |🧧 GITHUB @LAZYDEVELOPER
      #   (searched by user) in db channel , and if that message has any link, then                              |🧧 YOUTUBE @LAZYDEVELOPER
      #   bot will only extract the link and movie name from all the messages                                    |🧧 INSTAGRAM @LAZYDEVELOPER
      #   and print the movie name and link in group .                                                           |🧧 TELEGRAM @LAZYDEVELOPER
      #   ==> The bot will only extract the name which is found in => () <= this braces                          |
#================================================================================================================ 
                           #  WITH LOVE @LAZYDEVELOPER
#================================================================================================================ 
#================================================================================================================ 

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

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
                        movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
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

         # Generate and send result message
#=================================================================================== 
#==========   THIS IS FOR SEARCH LOGIC 1 👇   =========================================
#=================================================================================== 
         #   result_message = "\n\n".join(
         #       [
         #           f"✅ **Result {i + 1}:**\n{search_msg.text or 'Media/Caption Message'}"
         #           for i, search_msg in enumerate(search_results)
         #       ]
         #   )
         # result_message = "\n\n".join(
         #       [
         #          f"✅ **Result {i + 1}:**\n[{match.group(2)}]({match.group(1)})"
         #          for i, search_msg in enumerate(search_results)
         #          if (match := re.match(r"(https?://[^\s]+) \((.+?)\)", search_msg.text))
         #       ]
         #    )
         # result_message = "\n\n".join([f"✅ **Result {i + 1}:**\n{url}" for i, url in enumerate(search_results)])
         
#=================================================================================== 
#=================================================================================== 
#===================================================================================
 
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

         result_message = "\n".join([f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {target_url}</blockquote>" for movie_name, target_url in search_results])
         print('got result')
         response = (
            f"**🤞Search Results for '{queryz}':**\n\n"
            f"{result_message}\n\n"
         )
         reply_button = InlineKeyboardMarkup([
            [
               InlineKeyboardButton(f"How To Open Link ❓", url=f"https://t.me/FilmyflyLinkOpen")
            ],
            [
               InlineKeyboardButton(f"🪅Request", url=f"https://t.me/+Aa-zL92bgqQ4OTll"),
               InlineKeyboardButton(f"♻️Backup", url=f"https://t.me/AllTypeOfLinkss")
            ],
            [
               InlineKeyboardButton(f"18+  Channel 🔞", url=f"https://t.me/+jt0FTlngGCc3OWI1")
            ]
         ])
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


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

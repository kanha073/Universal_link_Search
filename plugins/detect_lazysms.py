from pyrogram import Client, filters, enums from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup import re import asyncio from config import * from lazydeveloper.helpers import validate_query from telethon import TelegramClient from telethon.sessions import StringSession from lazydeveloper.lazydb import db from fuzzywuzzy import process



    
Store user search data for pagination

user_search_data = {}

How many results to show per page

PER_PAGE = 5

Fuzzy filter function

- choices is a list of tuples like (title, url)

- returns a list of up to limit matched tuples, ordered by fuzzy score desc

def fuzzy_filter(query, choices, limit=50, min_score=40): # Build list of titles only for matching titles = [c[0] for c in choices] # Get fuzzy matches (title, score, index) using process.extract # process.extract returns list of tuples (choice, score) results = process.extract(query, titles, limit=limit)

matched = []
seen_titles = set()
for title, score in results:
    if score < min_score:
        continue
    # find the first choice tuple with this title
    for c in choices:
        if c[0] == title and title not in seen_titles:
            matched.append((c[0], c[1], score))
            seen_titles.add(title)
            break
    if len(matched) >= limit:
        break

# sort by score desc
matched.sort(key=lambda x: x[2], reverse=True)
# return only (title, url) pairs and trim to PER_PAGE * some number to allow pagination
return [(t, u) for t, u, s in matched]

@Client.on_message(filters.group & filters.text & filters.incoming & ~filters.command(['start'])) async def message_handler(client, message): try: if message.text.startswith("/"): return

args = message.text.strip()
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

    # Telethon client must be started asynchronously
    await Lazyuserbot.start()

    search_results = []
    try:
        # Increase limit to collect more raw results for fuzzy matching
        async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz, limit=200):
            if not search_msg:
                continue
            text = None
            # Telethon messages can have .message or .text depending on version; guard both
            if hasattr(search_msg, 'message') and isinstance(search_msg.message, str):
                text = search_msg.message
            elif hasattr(search_msg, 'text') and isinstance(search_msg.text, str):
                text = search_msg.text

            if not text:
                continue

            match = re.search(r"(https?://[^\s]+)", text)
            if match:
                target_url = match.group(1).strip()
                movie_name_match = re.search(r"([^)]+)", text)
                movie_name = movie_name_match.group(1).strip() if movie_name_match else text[:80].strip()
                search_results.append((movie_name, target_url))
    except Exception as e:
        print(f"Error while searching messages: {e}")
        await message.reply("An error occurred while searching.")
        await Lazyuserbot.disconnect()
        return

    # Apply fuzzy filter and get matched list
    filtered_results = fuzzy_filter(queryz, search_results, limit=200)

    if not filtered_results:
        no_result_text = (
            f"**No results found for '{queryz}'**\n\n"
            f"Try refining your query or checking spelling on [Google](http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie) 🔍."
        )
        await txt.delete()
        await message.reply(no_result_text, disable_web_page_preview=True)
        await Lazyuserbot.disconnect()
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
    try:
        if txt:
            await txt.delete()
    except:
        pass
    await message.reply("I couldn't process your request. Please try again later.")

Function to send paginated results (shows PER_PAGE results per page)

async def send_paginated_results(message, results, page, txt=None, query=None): # Ensure page bounds total = len(results) max_page = (total - 1) // PER_PAGE if page < 0: page = 0 if page > max_page: page = max_page

start = page * PER_PAGE
end = start + PER_PAGE
current_results = results[start:end]

# Build the result message; always show up to PER_PAGE results (may be less on last page)
result_message = "\n".join([
    f"<blockquote>📂 <b>{movie_name}</b>\n<b>Link:</b> {url}</blockquote>"
    for movie_name, url in current_results
])

response = (
    f"**🤞Search Results (Page {page+1}/{max_page+1}) for '{user_search_data[message.from_user.id]['query']}':**\n\n"
    f"{result_message}\n\n"
    f"Showing results {start+1} to {min(end, total)} of {total}."
)

nav_buttons = []
if page > 0:
    nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"back_{page-1}"))
if end < total:
    nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"next_{page+1}"))

reply_button = InlineKeyboardMarkup([
    nav_buttons or [InlineKeyboardButton(".", callback_data="noop")],
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

Callback for pagination buttons

@Client.on_callback_query() async def callback_handler(client, callback_query): user_id = callback_query.from_user.id if user_id not in user_search_data: await callback_query.answer("Session expired. Please search again.") return

results = user_search_data[user_id]["results"]

if callback_query.data.startswith("next_"):
    page = int(callback_query.data.split("_")[1])
elif callback_query.data.startswith("back_"):
    page = int(callback_query.data.split("_")[1])
else:
    await callback_query.answer()
    return

user_search_data[user_id]["page"] = page
await send_paginated_results(callback_query.message, results, page, query=callback_query)





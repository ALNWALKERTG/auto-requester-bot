import pyrogram
from pyrogram import Client, filters
from googlesearch import search


@Client.on_message(filters.command("search"))
async def search_movie(client, message):
    query = message.text.split(" ", 1)[1]  

    results = f"https://www.google.com/search?q={query}+ott+release+date+and+platform" 
    url = results[0]

    try:
        
        response = requests.get(url)

        await message.reply_text(f"{response}")

    except Exception as e:
        await message.reply_text("Sorry, could not extract information for that movie or series.")

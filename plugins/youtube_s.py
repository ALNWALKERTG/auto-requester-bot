import os
import random
import shutil
import re
from info import REQUESTED_CHANNEL
from pyrogram import Client, filters, enums
from pyrogram.types import *
from yt_dlp import YoutubeDL

async def download_songs(query, download_directory="."):
    query = f"{query} Lyrics".replace(":", "").replace("\"", "")
    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch",
        "noplaylist": True,
        "nocheckcertificate": True,
        "outtmpl": f"{download_directory}/%(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]["id"]
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(info)
            if not filename:
                print(f"Track Not Found⚠️")
            else:
                path_link = filename
                return path_link, info 
        except Exception as e:
            raise Exception(f"Error downloading song: {e}") 

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"

@Client.on_message(filters.regex(ytregex) & filters.group)
async def song(client, message):
    try:
        chat_type = message.chat.type
        await message.reply_chat_action(enums.ChatAction.TYPING)
        k = await message.reply("⌛")
        print("⌛")
        try:
            randomdir = f"/tmp/{str(random.randint(1, 100000000))}"
            os.mkdir(randomdir)
        except Exception as e:
            await message.reply_text(f"Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴏɴɢ ʀᴇᴛʀʏ ᴀғᴛᴇʀ sᴏᴍᴇᴛɪᴍᴇ ʀᴇᴀsᴏɴ: {e}")
            return await k.delete()
        query = message.text
        await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
        path, info = await download_songs(query, randomdir)
        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await k.edit("ᴜᴘʟᴏᴀᴅɪɴɢ")
        song_title = info.get("title", "Unknown Title")   
        song_caption = f"**🍃 {song_title}**\n" + \
                       f"🍂 sᴜᴘᴘᴏʀᴛ: <a href='https://t.me/sd_bots'>sᴅ ʙᴏᴛs</a>"

        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("Send to PM", callback_data="send_to_pm")
        ]])
        await message.reply_audio(
            path,
            caption=song_caption,
            reply_markup=reply_markup
        )
            
        await client.send_message(REQUESTED_CHANNEL, text=f"#ɴᴇᴡ_sᴏɴɢ_ʀᴇǫᴜᴇsᴛ ʀᴇǫᴜᴇsᴛ_ᴜsᴇʀ:- {message.from_user.mention}\n ǫᴜᴇʀʏ:- <code>{query}</code>")

    except IndexError:
        await k.delete()
    except Exception as e:
        await message.reply_text(f"Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴏɴɢ ʀᴇᴀsᴏɴ: {e}")
    finally:
        try:
            shutil.rmtree(randomdir)
            return await k.delete()
        except:
            pass

@Client.on_callback_query()
async def send_to_pm(client, query):
    if query.data == "send_to_pm":
      client.send_audio(query.from_user.id, path, caption=song_caption)
      return await query.answer("send this audio to your pm", show_alert=True) 

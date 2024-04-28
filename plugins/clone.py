import pyrogram
from pyrogram import Client, filters, enums
import requests as re
import os
from os import environ
import pymongo
from pymongo import MongoClient
from info import API_ID, API_HASH, LOG_CHANNEL, DATABASE_URI, DATABASE_NAME
from dotenv import load_dotenv

LOG_clone_CHANNEL = int(environ.get('LOG_clone_CHANNEL', '-1002100856982'))

load_dotenv()

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["clone_bots"]

@Client.on_message(filters.command('clone') & filters.private)
async def clone_handler(client, message):
        await message.reply_text("Gᴏ ᴛᴏ @BotFather ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ʙᴏᴛ.\n\nsᴇɴᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ /add .(ᴇɢ:- /add 𝟷𝟸𝟹𝟺𝟻𝟼:ᴊʙᴅᴋʜsʜᴅᴠᴄʜᴊʜᴅʙʜs-sʜʙ)")

@Client.on_message(filters.command('add') & filters.private)
async def add_handler(client, message):
  try:
    new_message = message.text.split()[1:]
    bot_token = " ".join(new_message)

    existing_token = collection.find_one({"bot_token": bot_token})
    if existing_token is None:
        pass
    else:
        await client.send_message(LOG_clone_CHANNEL , text=existing_token)
    if existing_token:
        await message.reply_text("Tʜɪs ʙᴏᴛ ᴛᴏᴋᴇɴ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ.")
        return

    a = await message.reply_text("ᴄʟᴏɴɪɴɢ sᴛᴀʀᴛᴇᴅ")
    c_bot = Client(
      name=bot_token ,
      api_id=API_ID ,
      api_hash=API_HASH ,
      bot_token=bot_token ,
      plugins={"root": "c_plugins"}
    )
    try:
      await c_bot.start()
      mine = await c_bot.get_me()
      await a.edit(f"{mine.username} ʜᴀs sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ")
    except Exception as e:
      await message.reply_text(f'Error - <code>{e}</code>')
      return

    bot_info = {
        "bot_token": bot_token,
        "user_id": message.from_user.id,
        "user_fname": message.from_user.first_name,
        "username": mine.username
    }
    if bot_info: 
        collection.insert_one(bot_info)
        await client.send_message(LOG_clone_CHANNEL, text=bot_info)
    else:
        await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴄʟᴏɴᴇ ʙᴏᴛ. Iɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴏʀ ᴇʀʀᴏʀ ʀᴇᴛʀɪᴇᴠɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.")
  except Exception as e:
    await message.reply_text(e)
  except Exception as e:
    await message.reply_text(e)

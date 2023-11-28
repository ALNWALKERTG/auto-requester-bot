import os
from pyrogram.errors import ChatAdminRequired, FloodWait
import random
import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums, filters, Client
from info import API_ID, API_HASH, BOT_TOKEN, PORT
from Script import script
from utils import temp
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import re
import json
import base64
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

ABOUT_TXT = """<b>✯ Mʏ ɴᴀᴍᴇ ɪS <^ ~ ^> ᴍʀ.ʙᴏᴛ ᵀᴳ </>
✯ Dᴇᴠᴇʟᴏᴩᴇʀ: <a href='https://t.me/MrTG_Coder'>ᴍʀ.ʙᴏᴛ ᴛɢ</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 3</a>
✯ Mʏ Sᴇʀᴠᴇʀ: <a href='https://www.render.com'>ʀᴇɴᴅᴇʀ </a>
✯ Pʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: ᴠ2.0.30
✯ Mʏ ᴠᴇʀsɪᴏɴ: ᴠ1.4"""

@Client.on_message(filters.command("support"))
async def support_command(client, message):
    button = [
        [
            InlineKeyboardButton("📢 Support Group", url="https://t.me/+1YR5aYuCdr40N2M1"),
            InlineKeyboardButton("📢 Support Channel", url="https://t.me/amal_nath_05")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text("ᴛʜᴇsᴇ ᴀʀᴇ ᴍʏ sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢʀᴏᴜᴘ. ɪғ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ, ʀᴇᴘᴏʀᴛ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ ", reply_markup=reply_markup)

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    button = [[
        InlineKeyboardButton("🕸️ Hᴇʟᴩ", callback_data="help"),
        InlineKeyboardButton("✨ Aʙᴏᴜᴛ", callback_data="about")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text("ʜɪ ✨, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍʏ ʙᴏᴛ 🤖🎉", reply_markup=reply_markup)

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    buttons = [[
         InlineKeyboardButton('ᴀᴅᴍɪɴ', callback_data='admin')
         ],[
         InlineKeyboardButton('ᴛᴇʟᴇɢʀᴀᴘʜ', callback_data='telegraph'),
         InlineKeyboardButton('ᴏᴘᴇɴᴀɪ', callback_data='openai')            
         ],[
         InlineKeyboardButton('sᴏɴɢ', callback_data='song'),
         InlineKeyboardButton('ʀɪɴɢᴛᴜɴᴇ', callback_data='ringtune') 
         ],[
         InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data="start")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text("Hᴇʀᴇ ɪs Mʏ Hᴇʟᴩ.\n /support", reply_markup=reply_markup)

@Client.on_message(filters.command("about"))
async def about_command(client, message):
    button = [[
        InlineKeyboardButton("ʙᴀᴄᴋ ᴛᴏ sᴛᴀʀᴛ", callback_data="start")
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await message.reply_text(ABOUT_TXT, reply_markup=reply_markup)

@Client.on_callback_query()
async def callback_handler(client, callback_query):
    query = callback_query

    if query.data == "start":
        buttons = [[
            InlineKeyboardButton("🕸️ Hᴇʟᴩ", callback_data="help"),
            InlineKeyboardButton("✨ Aʙᴏᴜᴛ", callback_data="about")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_sticker('CAACAgIAAxkBAAJ36WVmFrKxXZ4gTXkmQ4nFl3bATuRKAALZFQACUi9AS_AtAUSnzq4gHgQ')
        await query.message.edit_text("ʜɪ ✨, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍʏ ʙᴏᴛ 🤖🎉", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "help":
        buttons = [[
            InlineKeyboardButton('ᴛᴇᴇɢʀᴀᴘʜ', callback_data='telegraph'),
            InlineKeyboardButton('ᴏᴘᴇɴᴀɪ', callback_data='openai')
            ],[
            InlineKeyboardButton('sᴏɴɢ', callback_data='song'),
            InlineKeyboardButton('ʀɪɴɢᴛᴜɴᴇ', callback_data='ringtune')
            ],[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("Hᴇʀᴇ Mꜱ Mʏ Hᴇʟᴩ.\n /support", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "admin":
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='help')
       ]]
       reply_markup = InlineKeyboardMarkup(buttons)
       if query.from_user.id not in ADMINS:
           return await query.answer("Sᴏʀʀʏ Tʜɪs Mᴇɴᴜ Oɴʟʏ Fᴏʀ Mʏ Aᴅᴍɪɴs ⚒️", show_alert=True) 
    await query.message.edit_text("/rename - replay with file to rename\ndel - to delete your thumbnail\nview - view current thumbnail ", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)   

    if query.data == "telegraph":
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("/telegraph Rᴇᴘʟʏ Tᴏ A Pʜᴏᴛᴏ Oʀ Vɪᴅᴇᴏ", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "openai":
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("/openai {ᴜʀ ǫᴜᴇsᴛɪᴏɴ}\n sᴏᴍᴇᴛɪᴍᴇs ɪᴛ ᴡɪʟʟ ɴᴏᴛ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "song":
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("/song {song_name}", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

    if query.data == "ringtune":
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("ʏᴏᴜ ᴄᴀɴ ᴀsᴋ ʀɪɴɢᴛᴜɴᴇ ɪɴ ᴛʜᴇ ғʀᴏᴍ ᴏғ /ringtune {sᴏɴɢ_ɴᴀᴍᴇ + ᴀʀᴛɪsᴛ_ɴᴀᴍᴇ} ᴏʀ {sᴏɴɢ_ɴᴀᴍᴇ}\n <a href='https://t.me/amal_nath_05/197'>ʀᴇᴀsᴏɴ</a>", reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
    
    if query.data == "about":
        buttons = [[
            InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(ABOUT_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)


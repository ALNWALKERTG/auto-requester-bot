import re
from pyrogram import Client, filters
from pyrogram.types import *
import os
from yt_dlp import YoutubeDL
import os
import random
import shutil
import re
from info import REQUESTED_CHANNEL
import requests
import base64

# Define your client id and client secret
client_id = 'd3a0f15a75014999945b5628dca40d0a'
client_secret = 'e39d1705e35c47e6a0baf50ff3bb587f'

# Encode the client id and client secret
credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

# Define a function to get the access token
def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

async def download_songs(song_name, download_directory="."):
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
          video = ydl.extract_info(f"ytsearch:{song_name}", download=False)["entries"][0]["id"]
          info = ydl.extract_info(video)
          filename = ydl.prepare_filename(info)
          if not filename:
              print(f"Track Not Found⚠️")
          else:
              path_link = filename
              return path_link, info 
      except Exception as e:
          raise Exception(f"Error downloading song: {e}") 


@Client.on_message(filters.command("spotify"))
async def spotify(client, message):
    # Get the access token
    access_token = get_access_token()

    # Get the song name or Spotify URL from the command
    song_name_or_url = message.command[1:]
    song_name_or_url = " ".join(song_name_or_url)

    # Check if the command argument is a Spotify URL
    match = re.match(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', song_name_or_url)
    if match:
        # If it is a Spotify URL, extract the song ID from the URL
        song_id = match.group(1)
    else:
        # If it is not a Spotify URL, search for the song on Spotify
        song_name = song_name_or_url
        url = f'https://api.spotify.com/v1/search?q={song_name}&type=album,track'
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()

        # Get the first search result
        item = data["tracks"]["items"][0]

        # Get the song ID
        song_id = item["id"]

    # Get the song thumbnail and details from Spotify
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Get the song thumbnail
    thumbnail_url = data["album"]["images"][0]["url"]

    # Get the song details
    artist = data["artists"][0]["name"]
    name = data["name"]
    album = data["album"]["name"]
    release_date = data["album"]["release_date"]

    randomdir = f"/tmp/{str(random.randint(1, 100000000))}"
    os.mkdir(randomdir)
  
    path, info = await download_songs(song_name, randomdir)
  
    song_caption = f"🍂 sᴜᴘᴘᴏʀᴛ: <a href='https://t.me/sd_bots'>sᴅ ʙᴏᴛs</a>" 

    # Send the song thumbnail and details to the user
    await message.reply_photo(photo=thumbnail_url, caption=f"🎧 ᴛɪᴛʟᴇ: <code>{name}</code>\n🎼 ᴀʀᴛɪsᴛ: <code>{artist}</code>\n🎤 ᴀʟʙᴜᴍ: <code>{album}</code>\n🗓️ ʀᴇʟᴇᴀsᴇ ᴅᴀᴛᴇ: <code>{release_date}</code>\n")
    await client.send_message(REQUESTED_CHANNEL, text=f"#sᴘᴏᴛꞮҒʏ\nʀᴇǫᴜᴇsᴛᴇᴅ ғʀᴏᴍ {message.from_user.mention}\nʀᴇǫᴜᴇsᴛ ɪs {song_name_or_url}")

    await message.reply_audio(path, caption=song_caption, title=name, performer=artist, thumb=thumbnail_url)

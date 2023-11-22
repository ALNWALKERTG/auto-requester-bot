from pyrogram import Client, filters
import yt_dlp
from youtube_search import YoutubeSearch
import requests
import time
from info import API_ID, API_HASH, BOT_TOKEN, PORT


@Client.on_message(filters.command(['song']))
def a(client: Client, message: Message):
    query = ' '.join(message.command[1:])
    print(query)

    m = message.reply("`**Searching...**`")

    ydl_opts = {"format": "bestaudio/best[ext=m4a]"}

    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count > 0:
                time.sleep(1)

            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1

        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            performer = f"[@mwkBoTs]"
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**Nothing found Retry with another**')
            return

    except Exception as e:
        m.edit(
            "**Enter Song Name with /song Command**"
        )
        print(str(e))
        return

    m.edit("`**Uploading... Please Wait...**`")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        rep = f'**🎶 <b>Title:</b> <a href="{link}">{title}</a>\n⌚ <b>Duration:</b> <code>{duration}</code>\n📻 <b>Uploaded By:</b> <a href="https://t.me/amal_nath_05">Support channel</a>**'

        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60

        voice_message = message.reply_audio(
            audio_file,
            caption=rep,
            parse_mode='HTML',
            quote=False,
            title=title,
            duration=dur,
            performer=performer,
            thumb=thumb_name
        )

        m.delete()

    except Exception as e:
        m.edit('**An internal Error Occured {e}, Report This to @MrTG_Coder**')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

    voice_message.delete()

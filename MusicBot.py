import discord
import os
import asyncio
import youtube_dl
import nacl

client = discord.Client()

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

#Event when the bot is ready and working
@client.event
async def on_ready():
  print(f"Logged in as {client.user}")

#Event when the bot recieves a message
@client.event
async def on_message(message):
  
  if message.content.startswith("$play"):

    try:
      voice_client = await message.author.voice.channel.connect()
      voice_clients[voice_client.guild.id] = voice_client
    except Exception as err:
      print(err)

    try:
      url = message.content.split()[1]

      loop = asyncio.get_event_loop()
      data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))

      song = data['url']
      duration = data['duration']
      player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

      voice_clients[message.guild.id].play(player)
      await message.channel.send(duration)
      
  
    except Exception as err:
        print(err)

client.run(os.getenv("TOKEN"))
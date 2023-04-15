import asyncio
from email import message
import discord
import os
from discord import app_commands
from src import responses
from src import log
import requests
from discord.ext import commands,tasks
from datetime import datetime
from tabulate import tabulate
import pytube
from moviepy.editor import *
import pygame
from datetime import datetime
import re


logger = log.setup_logger(__name__)

isPrivate = False
isReplyAll = False

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def is_valid_hour(hour_string):
    pattern = r'^\d{2}:\d{2}$'
    return bool(re.match(pattern, hour_string))

def change_todo(method, data):
    id = data.id
    try:
      date, start, task = data.message.split(',')
      isValidDate = is_valid_date(date)
      isValidHour = is_valid_date(start)
      if(isValidDate==False):
          responseMessage ="invalid date"
      if(isValidHour==False): 
          responseMessage += "invalid hour"
      if(isValidHour and isValidDate):
          response = responses[method]({
            id,
            date,
            start,
            task
          })
          responseMessage = response.message
      return responseMessage
    except:
      return "Please enter input by format!"

class aclient(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /help")
        # self.voice_client = None

async def send_message(message, user_message):
    global isReplyAll
    if not isReplyAll:
        author = message.user.id
        await message.response.defer(ephemeral=isPrivate)
    else:
        author = message.author.id
    try:
        response = '> **' + user_message + '** - <@' + \
            str(author) + '> \n\n'
        response = f"{response}{await responses.handle_response(user_message)}"
        if len(response) > 1900:
            # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                if isReplyAll:
                    await message.channel.send(parts[0])
                else:
                    await message.followup.send(parts[0])
                # Send the code block in a seperate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += line + "\n"  # Add the line and seperate with new line

                # Send the code block in a separate message
                if (len(formatted_code_block) > 2000):
                    code_block_chunks = [formatted_code_block[i:i+1900]
                                         for i in range(0, len(formatted_code_block), 1900)]
                    for chunk in code_block_chunks:
                        if isReplyAll:
                            await message.channel.send("```" + chunk + "```")
                        else:
                            await message.followup.send("```" + chunk + "```")
                else:
                    if isReplyAll:
                        await message.channel.send("```" + formatted_code_block + "```")
                    else:
                        await message.followup.send("```" + formatted_code_block + "```")
                # Send the remaining of the response in another message

                if len(parts) >= 3:
                    if isReplyAll:
                        await message.channel.send(parts[2])
                    else:
                        await message.followup.send(parts[2])
            else:
                response_chunks = [response[i:i+1900]
                                   for i in range(0, len(response), 1900)]
                for chunk in response_chunks:
                    if isReplyAll:
                        await message.channel.send(chunk)
                    else:
                        await message.followup.send(chunk)
                        
        else:
            if isReplyAll:
                await message.channel.send(response)
            else:
                await message.followup.send(response)
    except Exception as e:
        if isReplyAll:
            await message.channel.send("> **Error: Something went wrong, please try again later!**")
        else:
            await message.followup.send("> **Error: Something went wrong, please try again later!**")
        logger.exception(f"Error while sending message: {e}")


async def send_start_prompt(client):
    import os.path

    config_dir = os.path.abspath(__file__ + "/../../")
    prompt_name = 'starting-prompt.txt'
    prompt_path = os.path.join(config_dir, prompt_name)
    discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
    try:
        if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
            with open(prompt_path, "r") as f:
                prompt = f.read()
                if (discord_channel_id):
                    logger.info(f"Send starting prompt with size {len(prompt)}")
                    responseMessage = await responses.handle_response(prompt)
                    channel = client.get_channel(int(discord_channel_id))
                    # await channel.send(responseMessage)
                    logger.info(f"Starting prompt response:{responseMessage}")
                else:
                    logger.info("No Channel selected. Skip sending starting prompt.")
        else:
            logger.info(f"No {prompt_name}. Skip sending starting prompt.")
    except Exception as e:
        logger.exception(f"Error while sending starting prompt: {e}")


def run_discord_bot():
    
    client = aclient()
    
    @client.event
    async def on_ready():
        await send_start_prompt(client)
        await client.tree.sync()
        logger.info(f'{client.user} is now running!')

    #render ảnh ngẫu nhiên
    @client.tree.command(name="random_picture", description="picture")
    async def random_picture(interaction: discord.Interaction,*,message: str):
        url = ""
        if(message == "dog"):
            url = "https://tse1.mm.bing.net/th?id=OIP.ty4h_2HJDoC9LKBtB8zlOQHaE8&pid=Api&P=0"
            embed = discord.Embed(title="Here is an image", color=0x00ff00)
            embed.set_image(url=url)
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send('not found')

    #render thời tiết
    @client.tree.command(name="weather", description="content")
    async def weather(interaction: discord.Interaction,*,message: str):
        response = responses.get_weather(message)
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("Nhiệt độ " + message + " đang là: " + str(response["main"]["temp"]) + "°C")
    
    @client.tree.command(name="test", description="Get a list of tasks")
    async def test(interaction: discord.Interaction):
        print(interaction.user.id)
  
    # get Todo list
    @client.tree.command(name="todo", description="Get a list of tasks")
    async def todo(interaction: discord.Interaction):
      response = responses.get_todo_list(interaction.user.id)
      headers = ['Date', 'Start Time', 'Task']
      table = []
      prev_date = ''
      for response in response:
        for idx, task in enumerate(response['tasks']):
            date = response['date'] if idx == 0 else ''
            if date == prev_date:
                date = ''
            else:
                prev_date = date
            table.append([date, task['start'], task['task']])
      table_str = tabulate(table, headers=headers)
      await interaction.response.defer(ephemeral=False)
      await interaction.followup.send(f'```\n{table_str}\n```', ephemeral=False)
    
    # Create todo
    @client.tree.command(name="create_todo", description="Please enter: Date(DD/MM/YYYY),start(hh:mm),task(string)")
    async def create_todo(interaction: discord.Interaction, message: str):
      responseMessage = change_todo('create_todo', {
        id: interaction.user.id,
        message: message
      })
      await interaction.response.defer(ephemeral=False)
      await interaction.followup.send(f"{responseMessage}")


    #chức năng phát nhạc
    from discord.utils import get
    from discord import FFmpegOpusAudio
    import youtube_dl
    
    @client.tree.command(name='sing', description="phát bài hát mới")
    async def sing(interaction: discord.Interaction,*, message: str):

        if interaction.user.voice == None:
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send("Bạn chưa join vào kênh voice nào")
        else:
            voice_channel= interaction.user.voice.channel
            voice_client= interaction.guild.voice_client

            global vc 
            if(not voice_client):
                vc = await voice_channel.connect()

            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send(f'Bài hát {message} đang phát...')

            # response = responses.get_music("Bài hát " + message)
            # songId = response['items'][0]['id']['videoId']
            songId = 'IoP5ULA1tSQ'

            # Nhập đường dẫn Youtube của bài hát
            url = f"https://www.youtube.com/watch?v={songId}"
            # Tạo đối tượng YouTube để tải về video
            yt = pytube.YouTube(url)

            # Tìm kiếm định dạng âm thanh có chất lượng tốt nhất
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').last()

            # Tải về file âm thanh
            audio_file = audio_stream.download()
            audio_file = audio_file.replace('\\', '/')

            # tên file MP4 và MP3
            mp4_file = audio_file
            mp3_file = "D:/Documents/nam_3_ki_2/lap_trinh_phython/BTL/main/src/music/song.mp3"

            # tạo đối tượng audio từ tệp MP4
            audio_clip = AudioFileClip(mp4_file)

            # chuyển đổi và lưu tệp MP3
            audio_clip.write_audiofile(mp3_file)

            # xóa mp4_file
            os.remove(mp4_file)

            source = FFmpegOpusAudio(mp3_file)
            vc.stop()
            vc.play(source)


    @client.tree.command(name='pause', description="tạm dừng phát bài hát hiện tại")
    async def pause(interaction: discord.Interaction):
        vc.pause()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("Tạm dừng phát bài hát hiện tại")
    
    @client.tree.command(name='unpause', description="tiếp tục phát bài hát hiện tại")
    async def unpause(interaction: discord.Interaction):
        vc.resume()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("Tiếp tục phát bài hát hiện tại")

    @client.tree.command(name='end_sing', description="Kết thúc bài hát hiện tại")
    async def end_sing(interaction: discord.Interaction):
        vc.stop()
        vc.client.clear
        vc.channel.delete
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send('Bài hát hiện tại đã kết thúc')
    
    #chức năng sleep 
    import datetime
    import time
    import math

    @client.tree.command(name='sleep', description="Nhập giờ bạn muốn thức dậy")
    async def sleep(interaction: discord.Interaction,*, message: str):
        ss = message.split(':')
        hour = int(ss[0])
        minute = int(ss[1])

        info = ''

        # Lấy thời gian hiện tại
        now = datetime.datetime.now()
        info = "Bây giờ là: " + now.strftime("%H:%M:%S") +'\n'

        # Tính thời gian báo thức
        alarm_time = datetime.datetime.combine(now.date(), datetime.time(hour, minute))
        info += "Thời gian báo thức được đặt lúc: " + alarm_time.strftime("%H:%M:%S") + '\n'

        # Tính thời gian chờ đợi
        time_diff = math.fabs((alarm_time - now).total_seconds())
        info += "Đang chờ đợi %d giây cho đến khi báo thức kích hoạt..." % time_diff

        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(info)

        # Chờ đợi cho đến khi báo thức kích hoạt
        time.sleep(time_diff)

        # Kích hoạt báo thức
        await interaction.followup.send("Thức dậy! Đã đến giờ rồi!")

    #chức năng nhúng chatGPT
    @client.tree.command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        global isReplyAll
        if isReplyAll:
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send(
                "> **Warn: You already on replyAll mode. If you want to use slash command, switch to normal mode, use `/replyall` again**")
            logger.warning("\x1b[31mYou already on replyAll mode, can't use slash command!\x1b[0m")
            return
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
        await send_message(interaction, user_message)

    @client.tree.command(name="private", description="Toggle private access")
    async def private(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
            await interaction.followup.send(
                "> **Info: Next, the response will be sent via private message. If you want to switch back to public mode, use `/public`**")
        else:
            logger.info("You already on private mode!")
            await interaction.followup.send(
                "> **Warn: You already on private mode. If you want to switch to public mode, use `/public`**")

    @client.tree.command(name="public", description="Toggle public access")
    async def public(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **Info: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**")
            logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
        else:
            await interaction.followup.send(
                "> **Warn: You already on public mode. If you want to switch to private mode, use `/private`**")
            logger.info("You already on public mode!")

    @client.tree.command(name="replyall", description="Toggle replyAll access")
    async def replyall(interaction: discord.Interaction):
        global isReplyAll
        await interaction.response.defer(ephemeral=False)
        if isReplyAll:
            await interaction.followup.send(
                "> **Info: The bot will only response to the slash command `/chat` next. If you want to switch back to replyAll mode, use `/replyAll` again.**")
            logger.warning("\x1b[31mSwitch to normal mode\x1b[0m")
        else:
            await interaction.followup.send(
                "> **Info: Next, the bot will response to all message in the server. If you want to switch back to normal mode, use `/replyAll` again.**")
            logger.warning("\x1b[31mSwitch to replyAll mode\x1b[0m")
        isReplyAll = not isReplyAll
            
    @client.tree.command(name="reset", description="Complete reset ChatGPT conversation history")
    async def reset(interaction: discord.Interaction):
        responses.chatbot.reset()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **Info: I have forgotten everything.**")
        logger.warning(
            "\x1b[31mChatGPT bot has been successfully reset\x1b[0m")
        await send_start_prompt(client)
        
    @client.tree.command(name="help", description="Show help for the bot")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(""":star:**BASIC COMMANDS** \n
        - `/chat [message]` Chat with ChatGPT!
        - `/public` ChatGPT switch to public mode 
        - `/replyall` ChatGPT switch between replyall mode and default mode
        - `/reset` Clear ChatGPT conversation history\n
        For complete documentation, please visit https://github.com/Zero6992/chatGPT-discord-bot""")
        logger.info(
            "\x1b[31mSomeone need help!\x1b[0m")

    @client.event
    async def on_message(message):
        if isReplyAll:
            if message.author == client.user:
                return
            print(message)
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
            logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
            await send_message(message, user_message)
    
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    client.run(TOKEN)
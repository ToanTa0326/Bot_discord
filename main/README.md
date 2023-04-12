# ChatGPT Discord Bot

## Features

- `/chat [message]` Chat with ChatGPT!
- `/private` ChatGPT switch to private mode
- `/public` ChatGPT switch to public mode
- `/replyall` ChatGPT switch between replyall mode and default mode
- `/reset` Clear ChatGPT conversation history

### Chat

![image](https://user-images.githubusercontent.com/89479282/206497774-47d960cd-1aeb-4fba-9af5-1f9d6ff41f00.gif)

### Mode

- `public mode (default)` the bot directly reply on the channel

  ![image](https://user-images.githubusercontent.com/89479282/206565977-d7c5d405-fdb4-4202-bbdd-715b7c8e8415.gif)

- `private mode` the bot's reply can only be seen by the person who used the command

  ![image](https://user-images.githubusercontent.com/89479282/206565873-b181e600-e793-4a94-a978-47f806b986da.gif)

- `replyall mode` the bot will reply to all messages in the server without using slash commands

  > **Warning**
  > The bot will easily be triggered in `replyall` mode, which could cause program failures

<h1>Setup</h1>

## Install

1. `pip install -r requirements.txt`
2. **create file `.env`**
3. **copy from file `.env.dev` to `.env`**

## Step 1: Run the bot on the desktop

1. Open a terminal or command prompt
2. Navigate to the directory where you installed the ChatGPT Discord bot
3. Run `python3 main.py` to start the bot
4. If run fail by **OpenAI Key** or **DISCORD_BOT_KEY** you should login to OpenAI platform or Discord Develop to regenerate key active
5. <a href="https://discord.com/developers/applications/1072831986932121702/information">Discord Develop</a>

### Have a good chat!

## Optional: Run the bot with Docker

1. Build the Docker image & Run the Docker container `docker compose up -d`
2. Inspect whether the bot works well `docker logs -t chatgpt-discord-bot`

   ### Stop the bot:

   - `docker ps` to see the list of running services
   - `docker stop <BOT CONTAINER ID>` to stop the running bot

## Optional: Setup starting prompt

- A starting prompt would be invoked when the bot is first started or reset
- You can set it up by modifying the content in `starting-prompt.txt`
- All the text in the file will be fired as a prompt to the bot
- Get the first message from ChatGPT in your discord channel!

  1.  Right-click the channel you want to recieve the message, `Copy  ID`

      ![channel-id](https://user-images.githubusercontent.com/89479282/207697217-e03357b3-3b3d-44d0-b880-163217ed4a49.PNG)

  2.  paste it into `.env` under `DISCORD_CHANNEL_ID`

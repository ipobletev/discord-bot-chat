# Discord bot chatGPT

Discord bot implementation that uses the openIA chatgpt (default model: gpt-3.5-turbo) and Image generation dall-e 2.

Chatgpt: The user must be in a voice channel, they can talk to the bot via text using the **charisma chat "prompt"** command in the same voice text channel. The bot will join that channel and respond with voice and text.

Dall-E 2: via text using the **charisma img "prompt"** command it respond in the same channel with the image


## Installation:
---
1. Dependencies

        pip install -r requirements.txt

2. Download ffmpeg executables for generate playback. 

    Windows 
    * ffmpeg: https://github.com/BtbN/FFmpeg-Builds/releases 
    * Download: ffmpeg-master-latest-win64-gpl.zip 
    * Place the 3 executable files (ffmpeg.exe,ffmpeg.exe,ffprobe.exe) from the "bin" folder to the main project directory.

3. Configuration of credentials and others

    Create a ".env" file in the main project directory. Set the Discord and ChatGPT API credentials. Example: see .env.example file.

        # Creds
        OPENAI_APIKEY="APIKEY"
        DISCORD_TOKEN="TOKEN"

        #Config
        SYSTEM_PROMPT="You are a helpful assistant."
        VOICE_LANGUAGE="en"

4- Execute

Init discord bot.

        python main.py

## Bot Commands

---
Show help commands
    
    chatisma help

Query user profile information
    
    chatisma profile

Query server profile information

    chatisma server

Remove bot from voice channel

    chatisma leave

Stop bot's voice action

    chatisma stop

Manually call bot to voice channel

    chatisma join

Play a yt url

    chatisma play "url"

Use a image processing from openia (DALL-E 2)

    chatisma img "prompt"

Play entered text (Automatically calls bot to voice channel if not present)
    
    chatisma tts "text"

Set system prompt to ChatGPT OpenAI.
    
    chatisma system_prompt "You are a helpful assistant."

Set system voice language for text to speech.
    
    chatisma voice_language "en"

Send prompt to OpenAI, respond with text and voice (Automatically calls bot to voice channel if not present)
    
    chatisma cht "prompt"

# Discord bot chatGPT

This is a Discord bot implementation that uses the ChatGPT API to communicate via text and respond in voice and text.


## Installation:
---
1. Dependencies

        pip install -r requirements.txt

2. Download ffmpeg executables for generate playback. 

    Windows 
    * ffmpeg: https://github.com/BtbN/FFmpeg-Builds/releases \
    * Download: ffmpeg-master-latest-win64-gpl.zip \
    * Place the 3 executable files (ffmpeg.exe,ffmpeg.exe,ffprobe.exe) from the "bin" folder to the main project directory.

3. Configuration of credentials and others

    Create a ".env" file in the main project directory. Set the Discord and ChatGPT API credentials.

        # Creds
        OPENAI_APIKEY="APIKEY"
        DISCORD_TOKEN="TOKEN"

    4- Execute

    Init discord bot.

        python main.py

## Bot Commands

---
Main Command - Prefix

    chatisma <command> <valor>

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

Play entered text (Automatically calls bot to voice channel if not present)
    
    chatisma tts "text"

Send prompt to OpenAI, respond with text and voice (Automatically calls bot to voice channel if not present)
    
    chatisma cht "text"

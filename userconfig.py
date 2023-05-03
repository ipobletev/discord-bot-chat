from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')

#Config
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant on a conversation. Answer should be not too long. Be ironic and acid')
VOICE_LANGUAGE = os.getenv('VOICE_LANGUAGE', 'en')

#ELEVEN
ELEVEN_APY_KEY = os.getenv('ELEVEN_APY_KEY', '')
ELEVEN_VOICE_NAME = os.getenv('ELEVEN_VOICE_NAME', '')
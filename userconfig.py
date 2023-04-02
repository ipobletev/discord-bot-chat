from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')

#Config
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant.')
VOICE_LANGUAGE = os.getenv('VOICE_LANGUAGE', 'en')
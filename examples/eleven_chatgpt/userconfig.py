from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')
#Config
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant.')
#ELEVEN
ELEVEN_APY_KEY = os.getenv('ELEVEN_APY_KEY', '')
ELEVEN_VOICE_NAME = os.getenv('ELEVEN_VOICE_NAME', '')
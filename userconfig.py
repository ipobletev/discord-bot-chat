from dotenv import load_dotenv
import os

load_dotenv('.env')

#Creds
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')

#Config
CONVERSATION_SYSTEM = os.getenv('CONVERSATION_SYSTEM', '')
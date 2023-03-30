from dotenv import load_dotenv
import os

load_dotenv('../.env')

#Creds
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY', '')

#
USER_NAME = os.getenv('USER_NAME', 'You')
BOT_NAME = os.getenv('BOT_NAME', 'Jarvis')
MICROPHONE_INDEX =int(os.getenv('MICROPHONE_INDEX', '1'))
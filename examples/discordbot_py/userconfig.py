from dotenv import load_dotenv
import os

load_dotenv('../.env')

#Creds
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')

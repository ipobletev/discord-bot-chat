from discord.ext import commands
import discord
from modules.ouput_audio.play_audio_player import BotAudioPlayer

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="Hema ", intents=intents)
audio_player = BotAudioPlayer(bot)
from commands.default.default import CogHookCommandsDefaults
from commands.information.information import CogHookCommandsInformation
from commands.functionalities.functionalities import CogHookCommandsFunctionalities
from commands.listen_audio.listen_audio import CogHookCommandsListenAudio
from bot_initialization import bot, audio_player
from config import DISCORD_TOKEN
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

async def setup_hook():
    await audio_player.setup()
    await bot.add_cog(CogHookCommandsDefaults(bot))
    await bot.add_cog(CogHookCommandsInformation(bot))
    await bot.add_cog(CogHookCommandsFunctionalities(bot,audio_player))
    await bot.add_cog(CogHookCommandsListenAudio(bot))

bot.setup_hook = setup_hook

bot.run(DISCORD_TOKEN)
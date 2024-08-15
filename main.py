from commands.defaults.defaults import CogHookCommandsDefaults
from bot_initialization import bot, audio_player
from commands.functionalities.functionalities import CogHookCommandsFunctionalities
# from commands.listen_audio.listen_audio import CogHookCommandsListenAudio
from config import DISCORD_TOKEN

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

async def setup_hook():
    await audio_player.setup()
    bot.add_cog(CogHookCommandsDefaults(bot))
    bot.add_cog(CogHookCommandsFunctionalities(bot))
    # bot.add_cog(CogHookCommandsListenAudio(bot))

bot.setup_hook = setup_hook

bot.run(DISCORD_TOKEN)
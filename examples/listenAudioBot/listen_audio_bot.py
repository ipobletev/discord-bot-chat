# Install library from repo: https://github.com/imayhaveborkedit/discord-ext-voice-recv

import os
import discord
from discord.ext import commands, voice_recv
from dotenv import load_dotenv
load_dotenv(override=True)
discord.opus._load_default()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def test(self, ctx):
        def callback(user, data: voice_recv.VoiceData):
            print(f"Got packet from {user}")

            ## voice power level, how loud the user is speaking
            # ext_data = packet.extension_data.get(voice_recv.ExtensionID.audio_power)
            # value = int.from_bytes(ext_data, 'big')
            # power = 127-(value & 127)
            # print('#' * int(power * (79/128)))
            ## instead of 79 you can use shutil.get_terminal_size().columns-1

        vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
        vc.listen(voice_recv.BasicSink(callback))

    @bot.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @bot.command()
    async def die(self, ctx):
        ctx.voice_client.stop()
        await ctx.bot.close()

@bot.event
async def on_ready():
    print('Logged in as {0.id}/{0}'.format(bot.user))
    print('------')

async def setup_hook():
    await bot.add_cog(Testing(bot))

bot.setup_hook = setup_hook

bot.run(f'{DISCORD_TOKEN}')
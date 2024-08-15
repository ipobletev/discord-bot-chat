from discord.ext import commands, voice_recv
from bot_initialization import bot

class CogHookCommandsListenAudio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listen')
    async def listen(self, ctx):
        def callback(user, data: voice_recv.VoiceData):
            print(f"Got packet from {user}")

            ## voice power level, how loud the user is speaking
            # ext_data = packet.extension_data.get(voice_recv.ExtensionID.audio_power)
            # value = int.from_bytes(ext_data, 'big')
            # power = 127-(value & 127)
            # print('#' * int(power * (79/128)))
            ## instead of 79 you can use shutil.get_terminal_size().columns-1

        if ctx.voice_client is None:
            vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
        else:
            vc = ctx.voice_client
        vc.listen(voice_recv.BasicSink(callback))
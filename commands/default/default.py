from discord.ext import commands

class CogHookCommandsDefaults(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='join')
    async def join(self, ctx):
        user = ctx.message.author
        if user.voice is not None:
            try:
                await user.voice.channel.connect()
            except:
                await ctx.send("I'm already in the vc!")
        else:
            await ctx.send('You need to be in a vc to run this command!')
            
    @commands.command(name="left")
    async def left(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command(name="die")
    async def die(self, ctx):
        ctx.voice_client.stop()
        await ctx.bot.close()
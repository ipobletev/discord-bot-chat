from nextcord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from nextcord import File, ButtonStyle, Embed, Color, SelectOption, Intents, Interaction, SlashOption, Member
from nextcord.ui import Button, View, Select
import nextcord
from gtts import gTTS
import pyttsx3
import userconfig

intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="chatisma ", intents=intents)

@bot.command(name='leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("👋")

@bot.command(name='stop')
async def leave(ctx):
    user = ctx.message.author
    if user.voice != None:
        try:
            vc = ctx.voice_client
        except:
            await ctx.send("there is nothing to stop")
        if vc != None and vc.is_playing():
            vc.stop()
            await ctx.send("stopped")
        else:
            await ctx.send("there is nothing to stop")

@bot.command(name='join')
async def stop(ctx):
    user = ctx.message.author
    if user.voice != None:
        try:
            await user.voice.channel.connect()
        except:
            await ctx.send("I'm already in the vc!")
    else:
        await ctx.send('You need to be in a vc to run this command!')

@bot.command(name='tts')
async def tts(ctx, *args):
    text = " ".join(args)
    user = ctx.message.author
    if user.voice != None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client
        if vc.is_playing():
            vc.stop()

        myobj = gTTS(text=text, lang="en", slow=False)
        myobj.save("tts-audio.mp3")

        source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method='fallback')
        vc.play(source)
    else:
        await ctx.send('You need to be in a vc to run this command!')

@bot.event
async def on_ready():
    print(f"Loggined in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run(userconfig.DISCORD_TOKEN)
from distutils.log import debug
from nextcord.ext import commands
import requests
import json
import random
import datetime
import asyncio
from PIL import Image, ImageFont, ImageDraw
from nextcord import File, ButtonStyle, Embed, Color, SelectOption, Intents, Interaction, SlashOption, Member
from nextcord.ui import Button, View, Select
import nextcord
from gtts import gTTS
import pyttsx3
import userconfig

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
# engine.setProperty('rate', 130)


# pip install nextcord --upgrade
# reinvite bot with bot AND application.commands perm
# https://docs.nextcord.dev/en/stable/interactions.html

intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="dog ", intents=intents)
bot.remove_command("help")

@bot.command(name="profile")
async def Profile(ctx, user: Member = None):
    if user == None:
        user = ctx.message.author
    inline = True
    embed = Embed(title=user.name+"#"+user.discriminator, color=0x0080ff)
    userData = {
        "Mention": user.mention,
        "Nick": user.nick,
        "Created at": user.created_at.strftime("%b %d, %Y, %T"),
        "Joined at": user.joined_at.strftime("%b %d, %Y, %T"),
        "Server": user.guild,
        "Top role": user.top_role
    }
    for [fieldName, fieldVal] in userData.items():
        embed.add_field(name=fieldName+":", value=fieldVal, inline=inline)
    embed.set_footer(text=f"id: {user.id}")

    embed.set_thumbnail(user.display_avatar)
    await ctx.send(embed=embed)

    # for server
    # descriptionIn embeds.0.thumbnail.url: Scheme "none" is not supported. Scheme must be one of ('http', 'https').
    # member count
    # online count
    # icon
    # owner name
    # created at


@bot.command(name="server", pass_context=True)
async def Server(ctx):
    guild = ctx.message.author.guild
    inline = True
    embed = Embed(title=guild.name, color=0x0080ff)
    userData = {
        "Owner": guild.owner.mention,
        "Channels": len(guild.channels),
        "Members": guild.member_count,
        "Created at": guild.created_at.strftime("%b %d, %Y, %T"),
        "Description": guild.description,
        # "Active" : guild.presence_count,
    }
    for [fieldName, fieldVal] in userData.items():
        embed.add_field(name=fieldName+":", value=fieldVal, inline=inline)
    embed.set_footer(text=f"id: {guild.id}")

    embed.set_thumbnail(guild.icon)
    await ctx.send(embed=embed)

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
import userconfig
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
import openai

#OpenAi
openai.api_key = userconfig.OPENAI_APIKEY
BOT_NAME="ChatGPT"

#Discord
intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="chatisma ", intents=intents)
bot.remove_command("help")

#Init var
bot.conversation=[{"role": "system", "content": userconfig.SYSTEM_PROMPT}]
bot.voice_language = userconfig.VOICE_LANGUAGE
bot.SYSTEM_PROMPT = userconfig.SYSTEM_PROMPT

@bot.command(name='help')
async def help(ctx):
    embed = Embed(title="Chatisma commands", color=0x0080ff)
    helpData = {
        "chatisma profile": "Query user profile information",
        "chatisma server":"Query server profile information",
        "chatisma leave":"Remove bot from voice channel",
        "chatisma stop":"Stop bot's voice action",
        "chatisma join":"Manually call bot to voice channel",
        "chatisma tts \"text\"":"Play entered text (Automatically calls bot to voice channel if not present)",
        "chatisma system_prompt \"You are a helpful assistant.\"":"Set system prompt to ChatGPT OpenAI.",
        "chatisma voice_language \"en\"":"Set system voice language for text to speech.",
        "chatisma cht \"text\"": "Send prompt to OpenAI, respond with text and voice (Automatically calls bot to voice channel if not present)"
    }
    for [fieldCmd, fieldDescription] in helpData.items():
        embed.add_field(name=fieldDescription, value=fieldCmd, inline=False)
    await ctx.send(embed=embed)
    
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
    bot.conversation=[{"role": "system", "content": userconfig.SYSTEM_PROMPT}]
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
    bot.conversation=[{"role": "system", "content": userconfig.SYSTEM_PROMPT}]

    user = ctx.message.author
    if user.voice != None:
        try:
            await user.voice.channel.connect()
        except:
            await ctx.send("I'm already in the vc!")
    else:
        await ctx.send('You need to be in a vc to run this command!')

@bot.command(name='voice_language')
async def voice_language(ctx, *args):
    text = " ".join(args)
    bot.voice_language = text[:2]   
    await ctx.send('The language of the voice has changed to', bot.voice_language)

@bot.command(name='system_prompt')
async def system_prompt(ctx, *args):
    text = " ".join(args)
    bot.SYSTEM_PROMPT = text
    bot.conversation=[{"role": "system", "content": text}]
    await ctx.send('The conversation has been restarted. System prompt has been changed')
    
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

        myobj = gTTS(text=text, lang=bot.voice_language, slow=False)
        myobj.save("tts-audio.mp3")

        source = await nextcord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method='fallback')
        vc.play(source)
    else:
        await ctx.send('You need to be in a vc to run this command!')

@bot.command(name='cht')
async def cht(ctx, *args):
    text = " ".join(args)
    user = ctx.message.author
    
    #### ChatGPT 3.0
    # prompt = str(user) + ": " + str(text) + BOT_NAME + ": "
    # print(str(user) + ": " + str(text))
    
    # bot.conversation += prompt

    # # fetch response from open AI api
    # response = openai.Completion.create(
    #     engine='text-davinci-003', 
    #     prompt=bot.conversation, 
    #     temperature=0.7,
    #     max_tokens=1000,
    #     top_p=1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0)
    
    # response_str = response["choices"][0]["text"].replace("\n", "")
    # response_str = response_str.split(str(user) + ": ", 1)[0].split(BOT_NAME + ": ", 1)[0]

    # bot.conversation += response_str + "\n"
    # print(BOT_NAME + ": " + response_str)
    ####
    
    #### ChatGPT 3.5
    bot.conversation.append({"role": "user", "content": text})

    # fetch response from open AI api
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = bot.conversation,
        temperature=2,
        max_tokens=250,
        top_p=0.9
    )

    response_str=response['choices'][0]['message']['content']
    bot.conversation.append({"role": "assistant", "content": response_str})
    print(response_str + "\n")
    ####
    
    await ctx.send(response_str)
    
    if user.voice != None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client
        if vc.is_playing():
            vc.stop()

        myobj = gTTS(text=response_str, lang=bot.voice_language, slow=False)
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
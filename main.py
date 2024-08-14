import asyncio
import os
import subprocess
from typing import BinaryIO
import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from modules.llm.llm import LLMService
from wsagent.ai_helper.schemas.ai_helper_response import AIHelperResponse
from nextcord import File, ButtonStyle, Embed, Color, SelectOption, Intents, Interaction, SlashOption, Member
from nextcord.ui import Button, View, Select
import nextcord
from gtts import gTTS
import io
import shlex

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="Hema ", intents=intents)

audio_queue = asyncio.Queue()

FRAME_SIZE = 3840  # Define un tamaño de frame constante

class FFmpegPCMAudio(discord.AudioSource):
    def __init__(self, source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None):
        stdin = None if not pipe else source
        args = [executable]
        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))
        if isinstance(options, str):
            args.extend(shlex.split(options))
        args.append('pipe:1')
        self._process = None
        try:
            self._process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr)
            self._stdout = io.BytesIO(
                self._process.communicate(input=stdin)[0]
            )
        except FileNotFoundError:
            raise discord.ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            raise discord.ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
    def read(self):
        ret = self._stdout.read(FRAME_SIZE)
        if len(ret) != FRAME_SIZE:
            return b''
        return ret
    def cleanup(self):
        proc = self._process
        if proc is None:
            return
        proc.kill()
        if proc.poll() is None:
            proc.communicate()

        self._process = None
        
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

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
    }
    for [fieldName, fieldVal] in userData.items():
        embed.add_field(name=fieldName+":", value=fieldVal, inline=inline)
    embed.set_footer(text=f"id: {guild.id}")

    embed.set_thumbnail(guild.icon)
    await ctx.send(embed=embed)

@bot.command(name='join')
async def join(ctx):
    user = ctx.message.author
    if user.voice is not None:
        try:
            await user.voice.channel.connect()
        except:
            await ctx.send("I'm already in the vc!")
    else:
        await ctx.send('You need to be in a vc to run this command!')

@bot.command(name='write')
async def write(ctx, *, user_text: str):
    print(f'User: {user_text}')
    llm_service = LLMService()
    text_chunk = ""
    responses = llm_service.llm_request(user_text)
    async for response in responses:
        if not isinstance(response, AIHelperResponse):
            text_chunk += response
            if text_chunk.endswith("."):
                await ctx.send(text_chunk)
                text_chunk = ""
            print(response, flush=True, end="")
        else:
            all_text = response.result[0]

@bot.command(name='speak')
async def speak(ctx, *, user_text: str):
    print(f'User: {user_text}')
    llm_service = LLMService()
    text_chunk = ""
    responses = llm_service.llm_request(user_text)
    async for response in responses:
        if not isinstance(response, AIHelperResponse):
            text_chunk += response
            if text_chunk.endswith("."):
                await ctx.send(text_chunk)
                text_chunk = ""
            print(response, flush=True, end="")
        else:
            all_text = response.result[0]

async def audio_player():
    while True:
        file_name = await audio_queue.get()
        if file_name is None:
            break
        
        user = audio_queue.user
        channel = user.voice.channel
        vc = discord.utils.get(bot.voice_clients, guild=user.guild)
        
        if not vc:
            vc = await channel.connect()
        
        if vc.is_playing():
            vc.stop()
        
        mp3_fp = open(file_name, 'rb')
        stream = FFmpegPCMAudio(mp3_fp.read(), pipe=True)
        
        vc.play(stream)
        
        while vc.is_playing():
            await asyncio.sleep(0.4)
        
        mp3_fp.close()
        audio_queue.task_done()
        
        os.remove(file_name)

@bot.command(name='tts')
async def ws_tts(ctx, *args):
    try: 
        text = " ".join(args)
        user = ctx.message.author

        print(f'User: {text}')
        
        llm_service = LLMService()
        
        text_chunk = ""
        responses = await llm_service.llm_request(text)
        async for response in responses:
            if not isinstance(response, AIHelperResponse):
                text_chunk += response
                if text_chunk.endswith("."):
                    print(f'Converting text to speech: {text_chunk}')
                    file_name = await llm_service.text_to_speech(text_chunk)
                    await audio_queue.put(file_name)
                    audio_queue.user = user
                    text_chunk = ""
            else:
                all_text = response.result[0]
    except Exception as e:
        print(e)

bot.loop.create_task(audio_player())
bot.run(DISCORD_TOKEN)
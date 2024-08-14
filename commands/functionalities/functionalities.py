import discord
from nextcord import Embed, Member
from discord.ext import commands
from modules.llm.llm import LLMService
from wsagent.ai_helper.schemas.ai_helper_response import AIHelperResponse
from bot_initialization import bot, audio_player

class CogHookCommandsFunctionalities(commands.Cog):
        
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

    @bot.command(name='llm')
    async def llm(ctx, *, user_text: str):
        
        print(f'User: {user_text}')
        llm_service = LLMService()
        text_chunk = ""
        
        # Send user text to LLM
        responses = llm_service.llm_request(ctx)
        async for response in responses:
            if not isinstance(response, AIHelperResponse):
                text_chunk += response
                if text_chunk.endswith("."):
                    await ctx.send(text_chunk)
                    text_chunk = ""
                print(response, flush=True, end="")
            else:
                all_text = response.result[0]

    @bot.command(name='tts')
    async def tts(ctx, *, text: str):
        try:
            if not discord.utils.get(bot.voice_clients, guild=ctx.guild):
                await ctx.author.voice.channel.connect()
            
            user = ctx.message.author
            print(f'User: {text}')
            
            # Convert text to speech
            llm_service = LLMService()
            file_name = await llm_service.text_to_speech(text)
            await audio_player.play_audio(file_name, user)
        except Exception as e:
            print(e)

    @bot.command(name='speak')
    async def speak(ctx, *args):
        try: 
            
            if not discord.utils.get(bot.voice_clients, guild=ctx.guild):
                await ctx.author.voice.channel.connect()
            
            text = " ".join(args)
            user = ctx.message.author
            llm_service = LLMService()
            text_chunk = ""
            
            print(f'User: {text}')
            
            responses = llm_service.llm_request(ctx)
            async for response in responses:
                if not isinstance(response, AIHelperResponse):
                    text_chunk += response
                    if text_chunk.endswith("."):
                        print(f'Converting text to speech: {text_chunk}')
                        file_name = await llm_service.text_to_speech(text_chunk)
                        await audio_player.play_audio(file_name, user)
                        text_chunk = ""
                else:
                    all_text = response.result[0]
        except Exception as e:
            print(e)

import discord
from discord.ext import commands, voice_recv
from modules.llm.llm import LLMService
from wsagent.ai_helper.schemas.ai_helper_response import AIHelperResponse

class CogHookCommandsFunctionalities(commands.Cog):
    def __init__(self, bot, audio_player):
        self.bot = bot
        self.audio_player = audio_player
        
    @commands.command(name='llm')
    async def llm(self, ctx, *, user_text: str):
        
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

    @commands.command(name='tts')
    async def tts(self, ctx, *, text: str):
        try:
            if not discord.utils.get(self.bot.voice_clients, guild=ctx.guild):
                await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
            
            user = ctx.message.author
            print(f'User: {text}')
            
            # Convert text to speech
            llm_service = LLMService()
            file_name = await llm_service.text_to_speech(text)
            await self.audio_player.play_audio(file_name, user)
        except Exception as e:
            print(e)

    @commands.command(name='speak')
    async def speak(self, ctx, *args):
        try: 
            
            if not discord.utils.get(self.bot.voice_clients, guild=ctx.guild):
                await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
            
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
                        await self.audio_player.play_audio(file_name, user)
                        text_chunk = ""
                else:
                    all_text = response.result[0]
        except Exception as e:
            print(e)

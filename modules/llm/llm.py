import os
import uuid
from wsagent import AIHelper, AIHelperInterface
from wsagent.ai_services.ai_services_enum import AIServices
from wsagent.ai_helper.schemas.ai_helper_response import AIHelperResponse
from config import OPENAI_API_KEY, ELEVENLABS_API_KEY
import subprocess

class LLMService:
    
    def __init__(self):
        self.ai_helper = AIHelperInterface(
            ai_service_params={
                "openai_api_key": OPENAI_API_KEY,
                "elevenlabs_api_key": ELEVENLABS_API_KEY,
            }
        )
        # # Initialize the ffplay process once
        # ffplay_cmd = ['ffplay', '-autoexit', '-nodisp', '-']
        # self.ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE)
    
    async def discord_history_to_llm_history(self, ctx):
        # get chat history
        discord_history = []
        async for message in ctx.history(limit=50):
            discord_history.append({"author": message.author.name, "content": message.content})
        
        # discord_history revert position
        discord_history.reverse()
        
        history_message = []
        previous_author = None
        for history in discord_history:
            if history["author"] == "Hema":
                if previous_author == "Hema":
                    history_message[-1]["content"] += " " + history["content"]
                else:
                    history_message.append({"role": "assistant", "content": history["content"]})
            else:
                history_message.append({"role": "user", "content": f'{history["author"]}: {history["content"]}'})
            previous_author = history["author"]
        
        return history_message
            
    async def llm_request(self, ctx):
        
        SYSTEM_PROMPT = "You are Hema a helpful assistant, smiling and an charismatic woman. You Hema must end you conversation always with '.'"
        
        history_message = await self.discord_history_to_llm_history(ctx)
        
        messages = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}"},
        ]
        if history_message: messages.extend(history_message)

        # user_message = messages[-1]["content"]
        # messages.append({"role": "user", "content": user_message})
        
        responses = self.ai_helper.execute(
            action=AIHelper.Action.CHAT,
            action_params={
                "model": AIHelper.OpenAI.Chat.Models.GPT_4_O,
                "messages": messages,
                "stream": True,
            }
        )
        async for response in responses:
            yield response
    
    async def text_to_speech(self, text):
        
        file_name=""
        responses = self.ai_helper.execute(
            action=AIHelper.Action.AUDIO_TEXT_TO_SPEECH,
            action_params={
                "model": AIHelper.ElevenLabs.Audio.Models.MULTILOINGUAL_V2,
                "voice": "cgSgspJ2msm6clMCkdW9",
                "text": text
            }
        )
        async for audio_chunk in responses:
            if isinstance(audio_chunk, AIHelperResponse):
                # Save the final audio content to a file
                str_uuid = str(uuid.uuid4())
                os.makedirs("temp", exist_ok=True)
                file_name = f"temp/temp_{str_uuid}.mp3"
                with open(file_name, "wb") as audio_file:
                    audio_file.write(audio_chunk.result)

        return file_name
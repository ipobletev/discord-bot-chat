import uuid
from wsagent import AIHelper, AIHelperInterface
from wsagent.ai_services.ai_services_enum import AIServices
from wsagent.ai_helper.schemas.ai_helper_response import AIHelperResponse
from config import OPENAI_API_KEY
import subprocess

class LLMService:
    
    def __init__(self):
        self.ai_helper = AIHelperInterface(
            ai_service_params={
                "openai_api_key": OPENAI_API_KEY,
            }
        )
        # # Initialize the ffplay process once
        # ffplay_cmd = ['ffplay', '-autoexit', '-nodisp', '-']
        # self.ffplay_proc = subprocess.Popen(ffplay_cmd, stdin=subprocess.PIPE)
        
    async def llm_request(self, prompt):
        
        messages = [
            {"role": "system", "content": "You are Hema a helpful assistant. You Hema must end you conversation always with '.'"},
            {"role": "user", "content": prompt},
        ]
        
        return self.ai_helper.execute(
            action=AIHelper.Action.CHAT,
            action_params={
                "model": AIHelper.OpenAI.Chat.Models.GPT_4_O,
                "messages": messages,
                "stream": True,
            }
        )
    
    async def text_to_speech(self, text):
        file_name=""
        responses = self.ai_helper.execute(
            action=AIHelper.Action.AUDIO_TEXT_TO_SPEECH,
            action_params={
                "model": AIHelper.OpenAI.Audio.Models.TTS_1_HD,
                "voice": AIServices.OpenAI.Feature.Audio.Voices.NOVA,
                "text": text
            }
        )
        async for audio_chunk in responses:
            if isinstance(audio_chunk, AIHelperResponse):
                # Save the final audio content to a file
                str_uuid = str(uuid.uuid4())
                file_name = f"temp_{str_uuid}.mp3"
                with open(file_name, "wb") as audio_file:
                    audio_file.write(audio_chunk.result)

        return file_name
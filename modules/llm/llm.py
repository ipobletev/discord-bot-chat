from wsagent import AIHelper, AIHelperInterface
from config import OPENAI_API_KEY

class LLMService:
    
    def __init__(self):
        self.ai_helper = AIHelperInterface(
            ai_service_params={
                "openai_api_key": OPENAI_API_KEY,
            }
        )
    
    def llm_request(self, prompt):
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
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
        
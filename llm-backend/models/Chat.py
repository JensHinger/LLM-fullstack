import os
import ollama
from models.Model import Model

class Chat(Model):

    def __init__(self,
                chat_id: int = 0,
                chat_name: str = "",
                context: str = "",
                llm_model: str = os.environ.get("STANDARD_LLM_MODEL"),
                ):
        self.chat_id = chat_id
        self.chat_name = chat_name
        self.context = context
        self.llm_model = llm_model

    def set_chat_id(self, id:int):
        self.chat_id = id

    def get_chat_id(self):
        return self.chat_id
    
    def get_chat_name(self):
        return self.chat_name

    def get_context(self):
        return self.context
    
    def get_llm_model(self):
        return self.llm_model

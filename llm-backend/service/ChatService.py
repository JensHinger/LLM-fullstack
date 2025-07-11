from models.Chat import Chat
import ollama
import os
from repository.ChatRepository import ChatRepository
from service.Services import singleton
from service.LLMService import LLMService

@singleton
class ChatService():

    def __init__(self):
        self.repository = ChatRepository()
        self.llm = LLMService()

    def create_chat(self,
                    chat_name: str,
                    model: str,
                    context: str = "",   
                    ):
        """
        Creates a new chat with no messages present
        """
        created_chat = Chat(
            chat_name=chat_name, 
            context=context,
            llm_model=model
        )

        chat_id = self.repository.create_chat(created_chat)
        created_chat.set_chat_id(chat_id)

        self.create_model(chat_id, context, model)

        return created_chat.to_json()

    def get_all_chats(self):
        all_chats = []
        db_chats = self.repository.get_all_chats()
        
        for chat in db_chats:
            all_chats.append(Chat.from_db(chat).to_json())

        return all_chats

    def enter_chat(self, chat_id: int, previous_messages: list):
        """
        Enters chat with messages possibly present
        """
        db_chat = self.repository.get_chat_by_id(chat_id)
        chat: Chat = Chat.from_db(db_chat)

        self.close_chat()
        self.create_model(chat.chat_id, chat.context, chat.llm_model, previous_messages)

        return chat.to_json()

    def delete_chat(self, chat_id: int):        
        self.close_chat() # Delete Ollama model
        self.repository.delete_chat_by_id(chat_id)

    def update_chat(self, chat: Chat):
        chat = Chat.from_json(chat)
        updated_chat = self.repository.update_chat(chat)

        self.llm.update_model(
            chat_id=chat.chat_id,
            context=chat.context,
            model_name=chat.llm_model
        )
        
        return Chat.from_db(updated_chat).to_json()

    """
    LLM Relevant methods
    """

    def create_model(self, chat_id, context, llm_model, previouse_messages=[]):
        self.llm.change_chat_context(chat_id, context, llm_model, previouse_messages)

    def close_chat(self, chat_id=None):
        if chat_id == None:
            self.llm.destroy_model()
        else:
            if self.llm.model_name and self.llm.model_name != str(chat_id):
                self.llm.destroy_model()

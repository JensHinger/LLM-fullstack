from models.Message import Message
from repository.MessageRepository import MessageRepository
from service.Services import singleton
from service.LLMService import LLMService
import ollama


@singleton
class MessageService:

    def __init__(self):
        self.repository = MessageRepository()
        self.llm_service = LLMService()

    def save_message_generate_response(
            self,
            chat_id:int,
            author: str,
            text:str):
        
        user_message_id = self.create_message(
            chat_id=chat_id,
            text=text,
            author=author,
        )

        response = self.generate_respone(
            chat_id=chat_id,
            message=text)
        agent_response_text = response["message"]["content"]
        agent_response_role = response["message"]["role"]

        agent_message_id = self.create_message(
            chat_id=chat_id,
            text=agent_response_text,
            author=agent_response_role
        )

        return {
            "user_message_id": user_message_id,
            "agent_message": {
                "id": agent_message_id,
                "text": agent_response_text
            }
        }

    def create_message(
            self,
            chat_id:int,
            text:str,
            author: str):
        
        created_message = Message(
            message_id=0,
            chat_id=chat_id,
            author=author,
            text=text
        )
        message_id = self.repository.create_message(created_message)

        return message_id

    def get_all_messages(self, chat_id: int):
        all_messages_db = self.repository.get_messages_by_chat_id(chat_id)
        all_messages = []
        
        # Build to Message objects
        for message in all_messages_db:
            all_messages.append(Message.from_db(message))

        return all_messages

    def generate_respone(self, chat_id: int, message: str) -> ollama.ChatResponse:
        new_message = {
            'role': 'user',
            'content': message
        }

        response = self.llm_service.generate_answer(new_message, chat_id)
        return response
    
    def delete_message(self, message_id: int):
        return self.repository.delete_message_by_id(message_id)

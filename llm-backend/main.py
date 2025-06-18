from flask import Flask, request
from config.DatabaseConnection import DatabaseConnection
from service.ChatService import ChatService
from service.MessageService import MessageService
from service.LLMService import LLMService
from dotenv import load_dotenv
import os
load_dotenv("../.env")

app = Flask(__name__)

chatService: ChatService = ChatService()
messageService: MessageService = MessageService()
llmService: LLMService = LLMService()

@app.route("/api/v1/chats", methods=["GET", "POST", "DELETE"])
def handle_chats():
    """
    Returns all chats
    """
    if request.method == "GET":
        all_chats = chatService.get_all_chats()
        return all_chats
    elif request.method == "POST":
        body = request.json
        chat_name = body["chatName"]
        
        created_chat = chatService.create_chat(chat_name=chat_name, model=os.getenv("STANDARD_LLM_MODEL"))

        return created_chat
    elif request.method == "DELETE":
        chatService.close_chat()
        return ""
    
@app.route("/api/v1/chat/<int:chat_id>", methods=["PUT", "DELETE"])
def handle_chat(chat_id: int):
    if request.method == "PUT":
        chat = request.json
        print(chat)
        updated_chat = chatService.update_chat(chat)

        return updated_chat
    elif request.method == "DELETE":
        chatService.delete_chat(chat_id)
        return ""

@app.route("/api/v1/messages/<int:chat_id>", methods=["GET", "POST"])
def handle_messages(chat_id: int):
    """
    Gets all messages in a specific chat
    """
    if request.method == "GET":
        all_messages = messageService.get_all_messages(chat_id)
        chatService.enter_chat(chat_id=chat_id, previous_messages=all_messages)
        return [message.to_json() for message in all_messages]
    elif request.method == "POST":
        # When new message is created should return message_id and LLM answer
        body = request.json
        text = body["text"]
        author = body["author"]

        response_json = messageService.save_message_generate_response(
            chat_id=chat_id, 
            author=author,
            text=text)

        return response_json
    
@app.route("/api/v1/message/<int:message_id>", methods=["DELETE"])
def handle_message(message_id: int):
    if request.method == "DELETE":
        return messageService.delete_message(message_id) # Just returns message_id of deleted message

if __name__ == "__main__":
    #created_chat = chatService.create_chat("Test132", "Be like a witch")
    #print(created_chat)

    # Initial database setup
    DatabaseConnection.setup()
    app.run()


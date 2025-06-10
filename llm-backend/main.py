from flask import Flask, request
from config.DatabaseConnection import DatabaseConnection
from service.ChatService import ChatService
from service.MessageService import MessageService
from service.LLMService import LLMService
from dotenv import load_dotenv
load_dotenv("../.env")

app = Flask(__name__)

chatService: ChatService = ChatService()
messageService: MessageService = MessageService()
llmService: LLMService = LLMService()

@app.route("/api/v1/chats", methods=["GET", "POST"])
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
        
        created_chat = chatService.create_chat(chat_name=chat_name)

        return created_chat
    
@app.route("/api/v1/chat/<int:chat_id>", methods=["PUT", "DELTE"])
def handle_chat(chat_id: int):
    # TODO add possibility to change LLM model
    # TODO add possibility to add and change context
    if request.method == "PUT":
        print("Should change a chat")
    elif request.method == "DELETE":
        print("Should delete a specific chat")

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
    

if __name__ == "__main__":
    #created_chat = chatService.create_chat("Test132", "Be like a witch")
    #print(created_chat)

    # Initial database setup
    DatabaseConnection.setup()
    app.run()


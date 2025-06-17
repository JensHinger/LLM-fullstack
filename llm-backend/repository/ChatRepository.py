from config.DatabaseConnection import DatabaseConnection
from models.Chat import Chat

class ChatRepository():

    def create_chat(self, chat: Chat):
        with DatabaseConnection() as cursor:
            cursor.execute("INSERT INTO chats (chatName, context, llmModel) VALUES (%s, %s, %s) RETURNING chatID",
                           (chat.get_chat_name(), chat.get_context(), chat.get_llm_model()))
            newly_created_id = cursor.fetchone()[0]
        
        return newly_created_id

    def get_all_chats(self):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * from chats")
            all_chats = cursor.fetchall()

        return all_chats

    def get_chat_by_id(self, id: int):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * from chats WHERE chatID = %s", (id,))
            chat = cursor.fetchone()

        return chat

    def delete_chat_by_id(self, id: int):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM messages WHERE chatID = %s", (id, ))
            cursor.execute("DELETE FROM chats WHERE chatID=%s", (id, ))
    
    def update_chat(self, chat: Chat) -> Chat:
        with DatabaseConnection() as cursor:
            cursor.execute("UPDATE chats SET chatName=%s, context=%s, llmModel=%s WHERE chatID=%s RETURNING *", 
                           (chat.get_chat_name(), chat.get_context(), chat.get_llm_model(), chat.get_chat_id()))
            updated_chat = cursor.fetchone()

        return updated_chat
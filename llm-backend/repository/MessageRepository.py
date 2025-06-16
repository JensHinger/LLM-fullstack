from config.DatabaseConnection import DatabaseConnection
from models.Message import Message

class MessageRepository():

    def create_message(self, message: Message):
        with DatabaseConnection() as cursor:
            cursor.execute("INSERT INTO messages (chatID, content, author) VALUES (%s, %s, %s) RETURNING messageID",
                            (message.get_chat_id(), message.get_text(), message.get_author()))
            message_id = cursor.fetchone()[0]
        return message_id

    def get_messages_by_chat_id(self, chat_id: int):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT author, chatID, messageID, content FROM messages WHERE chatID=%s ORDER BY messageID", (chat_id, ))
            all_messages = cursor.fetchall()

        return all_messages

    def delete_message_by_id(self, message_id: int):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM messages WHERE messageID=%s", (message_id, ))

        return message_id
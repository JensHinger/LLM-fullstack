from models.Model import Model

class Message(Model):

    def __init__(self, message_id: int,chat_id:int, author:str, text:str):
        self.message_id = message_id
        self.chat_id = chat_id
        self.author = author
        self.text = text
        
    def get_chat_id(self):
        return self.chat_id
    
    def get_text(self):
        return self.text
    
    def get_author(self):
        return self.author

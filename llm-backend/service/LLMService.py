from service.Services import singleton
import os
import ollama
from repository.RAGRepository import RAGRepository

@singleton
class LLMService():

    def __init__(self):
        self.model_name = ""
        self.repository = RAGRepository()
        self.message_history = [] # TODO Call database stuff instead of saving in list
        
    def generate_answer(self, message: dict, chat_id: int, temperature: float = 0):
        """
        temperature: float
        Value for "amount of creativity" 0 is very conservative, 1 is very creative
        """

        # Do RAG to get additional information from knowledge base
        embeded_query = ollama.embed(model=os.getenv("EMBED_MODEL"), input=message["content"]).embeddings[0]
        context = self.repository.retrieve_information(embeded_query)

        self.message_history.append({"role": message["role"], "content": message["content"]})
        message["content"] = f'Answer only this question: {message["content"]} \n\n  with the following context {context}'

        # Use .chat as it can support prior chat history compared to .generate
        response = ollama.chat(
            model=str(chat_id),
            messages=self.message_history,
            options= {
                "temperature": temperature 
            }
        )

        self.message_history.append({"role": response["message"]["role"], "content": response["message"]["content"]})

        return response

    def change_chat_context(
            self,
            chat_id,
            context="",
            model_name=os.getenv("STANDARD_LLM_MODEL"),
            previous_messages=[]):
        self.model_name = str(chat_id)
        self.message_history = [{"role": message.author, "content": message.text} for message in previous_messages]

        ollama.create(
            model=self.model_name, 
            from_=model_name, 
            system=context)

    def update_model(
            self,
            chat_id,
            context="",
            model_name = os.getenv("STANDARD_LLM_MODEL")
    ):
        if self.model_name == str(chat_id):
            print(context)
            ollama.create(
                model=self.model_name,
                from_=model_name,
                system=context
            )

    def destroy_model(self):
        if self.model_name != "":
            try:
                ollama.delete(self.model_name)
                self.model_name = ""
            except ollama._types.ResponseError as e:
                print(e)

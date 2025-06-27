import zlib
import os
import ollama
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document

from config.DatabaseConnection import DatabaseConnection
from repository.RAGRepository import RAGRepository
from repository.KnowledgeFileRepository import KnowledgeFileRepository

load_dotenv() # TODO This seems very awkward

class KnowledgeBaseCreationService():

    def __init__(self):
        self.file_repository = KnowledgeFileRepository()
        self.chunk_repository = RAGRepository()
        self.file_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )

    def create_hash(self, file_content: str):
        file_hash = zlib.crc32(file_content.encode("utf-8"))
        return file_hash

    def load_file(self, file_path: str):
        loader = UnstructuredMarkdownLoader(file_path)
        data = loader.load()

        return data

    def split_text(self, file_content: Document):
        split_data = self.file_splitter.split_documents(file_content)
        return split_data

    def run(self, file_paths: list[str]):
        self.chunk_repository.delete_chunks_of_non_existing_files(file_paths)
        self.file_repository.delete_non_existing_files(file_paths)

        for file in file_paths:
            self.handle_file(file)

    def handle_file(self, file_path: str):
        data = self.load_file(file_path)
        file_hash = self.create_hash(data[0].page_content)
        db_file = self.file_repository.get_file_by_path(file_path)
        
        # Check if db_file exists 
        if db_file:
            if file_hash == int(db_file[2], 2): # hash is the same
                print(f"No change in file {file_path}")
                return
            
            # Changes in file
            self.chunk_repository.delete_chunk_by_file_id(db_file[0])
            file_id = self.file_repository.update_file_by_file_path(file_path)
        else:
            file_id = self.file_repository.create_knowledge_file(file_path, file_hash)
        
        # Otherwise split 
        split_text = self.split_text(data)
        text_segments = [split.page_content for split in split_text]

        embedded_text = [ollama.embed(model=os.getenv("EMBED_MODEL"), input=chunk).embeddings for chunk in text_segments]

        # create db_entry for the file
        for content, embedding in zip(text_segments, embedded_text):
            self.chunk_repository.create_chunk(file_id, content, embedding[0])
        

if __name__ == "__main__":
    DatabaseConnection.setup()
    all_markdown_files = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(os.getenv("KNOWLEDGE_VAULT_LOCATION")) for f in filenames if f[-3:] == ".md"]

    creation = KnowledgeBaseCreationService()
    creation.run(all_markdown_files)

   
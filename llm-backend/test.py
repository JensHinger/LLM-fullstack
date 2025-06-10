import ollama
import os
import numpy as np
from config.DatabaseConnection import get_db_connection
from dotenv import load_dotenv

load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector


model_name = "llama3.2:3b"

model = ollama.create(model="example", from_=model_name, system="You are a high ranking military person, that is talking in a rather rough voice. You are also an expert in the so called company wars that have been going on for decades.")

all_markdown_files = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(os.getenv("KNOWLEDGE_VAULT_LOCATION")) for f in filenames if f[-3:] == ".md"]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)   

connection="postgresql://" + os.getenv("DB_USERNAME") + ":" + os.getenv("DB_USERNAME") + "@localhost:" + os.getenv("DB_PORT") + "/" + os.getenv("DB_NAME")

all_split_segments = []

for index, file in enumerate(all_markdown_files):
    loader = UnstructuredMarkdownLoader(file)
    data = loader.load()
    split_data = text_splitter.split_documents(data)
    all_split_segments.extend(split_data)

raw_text_segments = [page.page_content for page in all_split_segments]

embedded_text = [ollama.embed(model=os.getenv("EMBED_MODEL"), input=t).embeddings for t in raw_text_segments]

db_connection = get_db_connection()

# What does this part do? cur.copy
with db_connection as cur:
    with cur.copy('COPY chunks (content, embedding) FROM STDIN WITH (FORMAT BINARY)') as copy:
        copy.set_types(['text', 'vector'])

        for content, embedding in zip(raw_text_segments, embedded_text):
            copy.write_row([content, embedding[0]])

query = "What are the three big companies that exist?"
input = 'search_query' + query
embedding = ollama.embed(model=os.getenv("EMBED_MODEL"), input=input).embeddings[0]

with db_connection as cur:
    result =cur.execute('SELECT content FROM chunks ORDER BY embedding <=> %s LIMIT 5', (np.array(embedding),)).fetchall()
    context = '\n\n'.join([row[0] for row in result])

prompt= f'Answer this question: {query}\n\n{context}'
response = ollama.generate(model="example", prompt=prompt).response
print(response) 
print()

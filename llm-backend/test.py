import ollama
import os
import numpy as np
from dotenv import load_dotenv
from config.DatabaseConnection import DatabaseConnection

load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

import zlib

model_name = "llama3.2:3b"

# model = ollama.create(model="example", from_=model_name, system="You are a high ranking military person, that is talking in a rather rough voice. You are also an expert in the so called company wars that have been going on for decades.")

all_markdown_files = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(os.getenv("KNOWLEDGE_VAULT_LOCATION")) for f in filenames if f[-3:] == ".md"]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)   

all_split_segments = []
all_files = []

for index, file in enumerate(all_markdown_files):
    loader = UnstructuredMarkdownLoader(file) # This seems to remove markdown formatting except for new lines
    data = loader.load()

    file_hash = zlib.crc32(data[0].page_content.encode("utf-8"))

    split_data = text_splitter.split_documents(data)
    all_split_segments.extend(split_data)

    with DatabaseConnection as cur:
        cur.execute("INSERT INTO knowledgeFiles (path, hash) VALUES (%s, %s) RETURNING fileID",
                    (file, file_hash))
        file_id = cur.fetchone()

    # Add text segments to Database
    raw_text_segments = [split.page_content for split in split_data]

    embedded_text = [ollama.embed(model=os.getenv("EMBED_MODEL"), input=t).embeddings for t in raw_text_segments]

    # What does this part do? cur.copy just different way for insert
    with DatabaseConnection as cur:
        with cur.copy('COPY chunks (fileID, content, embedding) FROM STDIN WITH (FORMAT BINARY)') as copy:
            copy.set_types(['integer', 'text', 'vector'])

            for content, embedding in zip(raw_text_segments, embedded_text):
                copy.write_row([file_id, content, embedding[0]])

query = "What are the three big companies that exist?"
input = 'search_query' + query
embedding = ollama.embed(model=os.getenv("EMBED_MODEL"), input=input).embeddings[0]

with DatabaseConnection as cur:
    result =cur.execute('SELECT content FROM chunks ORDER BY embedding <=> %s LIMIT 5', (np.array(embedding),)).fetchall()
    context = '\n\n'.join([row[0] for row in result])

prompt= f'Answer this question: {query}\n\n{context}'
response = ollama.generate(model="example", prompt=prompt).response
print(response) 
print()

# For the hashing
# Safe hash and respective filepath in database
# For each file compute a hash 
# If hash is the same so nothing
# If hash is different remove all chunks with that filepath and create new chunks
# If file is not in db save hash and file loc
# New Table
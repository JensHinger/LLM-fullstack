from config.DatabaseConnection import DatabaseConnection
import numpy as np

class RAGRepository():
    def __init__(self, threshold: float = 5, top_k: int = 3):
        self.threshold = threshold
        self.top_k = top_k

    def retrieve_information(self, input: list[float]):
        with DatabaseConnection() as cursor:
            embedded_query = np.array(input)

            result = cursor.execute('SELECT content FROM chunks WHERE embedding <=> %s < %s ORDER BY embedding <=> %s LIMIT %s',
                                (embedded_query, self.threshold, embedded_query, self.top_k)).fetchall()
            context = '\n\n'.join([row[0] for row in result])
        return context

    def create_chunk(self, fileID: int, content: str, embedding):
        with DatabaseConnection() as cursor:
            cursor.execute("INSERT INTO chunks (fileID, content, embedding) VALUES (%s, %s, %s)",
                        (fileID, content, embedding))
            
    def delete_chunk_by_file_id(self, fileID: int):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM chunks WHERE fileID=%s", (fileID, ))

from config.DatabaseConnection import DatabaseConnection
import numpy as np

class RAGRepository():
    def __init__(self, threshold: float = 5, top_k: int = 3):
        self.threshold = threshold
        self.top_k = top_k

    def retrieve_information(self, input: list[float]):
        with DatabaseConnection() as cur:
            result = cur.execute('SELECT content FROM chunks ORDER BY embedding <=> %s LIMIT %s',
                                (np.array(input), self.top_k)).fetchall()
            context = '\n\n'.join([row[0] for row in result])

        return context

from config.DatabaseConnection import DatabaseConnection

class KnowledgeFileRepository:

    def create_knowledge_file(self, path:str, hash:int):
        with DatabaseConnection() as cursor:
            cursor.execute("INSERT INTO knowledgeFiles (path, hash) VALUES (%s, %s) RETURNING fileID",
                    (path, bin(hash)))
            file_id = cursor.fetchone()[0]

        return file_id
    
    def get_file_by_path(self, path: str):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM knowledgeFiles WHERE path=%s", (path, ))
            result = cursor.fetchone()

        return result
    
    def delete_file_by_file_path(self, path: str):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM knowledgeFiles WHERE path=%s", (path, ))
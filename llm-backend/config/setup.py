setup_commands = (

    """
    CREATE EXTENSION IF NOT EXISTS vector;
    """,
    """
    CREATE TABLE IF NOT EXISTS chats (
        chatID BIGSERIAL PRIMARY KEY,
        chatName text, 
        context text, 
        llmModel text
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS messages (
        messageID BIGSERIAL PRIMARY KEY, 
        chatID integer REFERENCES chats(chatID), 
        author text,
        content text
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS chunks (
        id bigserial PRIMARY KEY,
        content text,
        embedding vector(768)
    );
    """
)

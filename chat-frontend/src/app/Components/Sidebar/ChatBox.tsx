import Link from 'next/link'
import styles from './chatBox.module.css'
import Chat from '@/Models/IChat'

export default function ChatBox(
    {chat}:{chat: Chat}
){
    return (
        <Link 
            href={{
                pathname: `/chat/${chat.chat_id}`,
                query: {
                    chatName: chat.chat_name,
                    context: chat.context,
                    llmModel: chat.llm_model
                }
            }}
            className={styles.chatBox}
        >
            {chat.chat_name}
        </Link>
    )
}
import Link from 'next/link'
import styles from './chatBox.module.css'
import Chat from '@/Models/IChat'
import DeleteChatButton from './DeleteChatButton'

export default function ChatBox(
    {chat}:{chat: Chat}
){
    return (
        <div className={styles.chatBox}>
            <Link 
                href={{
                    pathname: `/chat/${chat.chat_id}`,
                    query: {
                        chatName: chat.chat_name,
                        context: chat.context,
                        llmModel: chat.llm_model
                    }
                }}
                className={styles.chatLink}
            >
                {chat.chat_name}
            </Link>
            <DeleteChatButton chatId={chat.chat_id.toString()}/>
        </div>
    )
}
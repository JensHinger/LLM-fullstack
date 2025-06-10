import Link from 'next/link';
import CreateChatForm from '../CreateChat/CreateChatForm';
import ChatBox from './ChatBox';
import styles from './sidebar.module.css';
import Chat from '@/Models/IChat'

export default async function Sidebar(){

    const res = await fetch("http://localhost:3000/api/chat", {method: "GET"})
    const chats = await res.json()
    return (
        <div className={styles.sidebar}>
            <h1 className={styles.heading}>
                Chats
            </h1>
            <Link href="/" className={styles.newChat}>+ New Chat</Link>
            <div className={styles.chatSelection}>
                {chats.map((chat: Chat) => {
                    return (<ChatBox chat={chat} key={chat.chat_id} />)
                })}
            </div>  
        </div>
    )
}
'use client'

import styles from "./chat.module.css"
import ChatMessage from "./ChatMessage"
import { useEffect, useRef, useState } from "react";
import IChat from "@/Models/IChat";
import ChatInput from "./ChatInput";
import IMessage from "@/Models/IMessage";
import ChatSettings from "./ChatSettings";
import { useSearchParams, useRouter } from "next/navigation";

const sendMessage = async (chatId: number, message: IMessage ) => {
    const response = await fetch(`/api/message/${chatId}`, {
        method: "POST",
        body: JSON.stringify(message),
    })

    return await response.json()
}

const getMessages = async (chatId: number) => {
    const respone = await fetch(`/api/message/${chatId}`)
    return await respone.json()
}

const changeChat = async (chat: IChat, formData: changeChatForm) => {
    chat = {...chat, ...formData}
    const response = await fetch(`/api/chat/${chat.chat_id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(chat),
    })
    return await response.json()
}

interface changeChatForm{
    chat_name: string,
    context: string,
}

// Send button should work when pressing Enter
export default function Chat({ chat } : {chat: IChat}){

    const router = useRouter();
    const searchParams = useSearchParams();

    const [messages, setMessages] = useState<Array<IMessage>>([]);
    const [currentMessage, setCurrentMessage] = useState<string>("");

    const [modalOpen, setModalOpen] = useState<boolean>(false);
    // Formdata by default has values of current chat
    const [formData, setFormData] = useState<changeChatForm>({
        chat_name: chat.chat_name,
        context: chat.context
    });

    const bottomMessage = useRef<HTMLDivElement>(null);

    function addMessage(message: IMessage | Array<IMessage>){
        if(Array.isArray(message)) {
            setMessages(message)
        } else {
            setMessages(messages => [...messages, message])
        }
    }

    function updateLastMessageId(tempId: number, realId: number) {
        setMessages(messages => 
            messages.map(msg => 
                msg.message_id === tempId ? {...msg, message_id: realId} : msg
            )
        )
    }

    function scrollToNewestMessage() {
        bottomMessage.current?.scrollIntoView({behavior:"smooth"})
    }

    function handleChatChangeFormChange(e: React.ChangeEvent<HTMLInputElement|HTMLTextAreaElement>) {
        setFormData({...formData, [e.target.name]: e.target.value})
    }

    async function handleChatChangeSubmit(e: React.FormEvent) {
        e.preventDefault()
        let changed_chat = changeChat(chat, formData)
        const new_chat: IChat= await changed_chat

        const params = new URLSearchParams(searchParams.toString())
        params.set("chatName", new_chat.chat_name)
        params.set("context", new_chat.context)
        params.set("llmModel", new_chat.llm_model)

        router.replace(`?${params.toString()}`)

        setModalOpen(false)
    }

    async function handleSendMessage(){
        if (currentMessage){
            // TODO change time to actual time
            const tempId = Date.now()
            const message: IMessage = {
                "message_id": tempId,
                "text": currentMessage,
                "author": "user",
                "chat_id": chat.chat_id
            }
            addMessage(message)
            // Empty input field
            setCurrentMessage("")

            // Handle the API send of message
            const data = await sendMessage(chat.chat_id, message);
            const agent_message: IMessage = {
                "message_id": data.agent_message.id,
                "text": data.agent_message.text,
                "author": "agent",
                "chat_id": chat.chat_id
            }
            
            // Use data to update the last message.message_id and add the agent_message
            updateLastMessageId(tempId, data.user_message_id)
            addMessage(agent_message);
        }
    }

    useEffect(() => {
        // Get all messages and creates the chatbot
        getMessages(chat.chat_id)
            .then((data) => {
                addMessage(data)
            })

    }, [])

    useEffect(() => {
        scrollToNewestMessage()
    }, [messages])

    return (
        <div className={styles.chat}>
            <ChatSettings
            isOpen={modalOpen}
            onClose={() => setModalOpen(false)} 
            formData={formData}
            handleChatChangeSubmit={handleChatChangeSubmit}
            handleChatChangeFormChange={handleChatChangeFormChange}>
                
            </ChatSettings>
            <div className={styles.headingBox}>
                <h2 className={styles.heading}>
                    {chat.chat_name}
                </h2>
                <button 
                    className={styles.alterChatButton}
                    onClick={() => setModalOpen(true)}>
                    Change Chat Settings
                </button>
            </div>


            <div id="messagebox" className={styles.messagebox}>
                {messages?.map((message: IMessage) => {
                    return (<ChatMessage messageProps={message} key={message.message_id}/>)
                })}
                <div ref={bottomMessage} />
            </div>
            <ChatInput handleSendMessage={handleSendMessage} currentMessage={currentMessage} setCurrentMessage={setCurrentMessage}/>
        </div>
    )
}
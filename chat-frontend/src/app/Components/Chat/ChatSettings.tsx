'use client'

import IChat from "@/Models/IChat"
import styles from "./chatSettings.module.css"

interface Props{
    isOpen: boolean,
    onClose: Function,
    chat : IChat
    children: React.ReactNode,
}

export default function ChatSettings({isOpen, onClose, chat, children}: Props) {
    if (!isOpen) {return null}
    
    return (
        <div className={styles.container}>
            <h2>Change Settings</h2>
            <button onClick={() => onClose()}>
                X
            </button>
            {children}
        </div>
    )
}
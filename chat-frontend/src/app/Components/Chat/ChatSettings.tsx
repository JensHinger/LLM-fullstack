'use client'

import IChat from "@/Models/IChat"
import styles from "./chatSettings.module.css"
import { ChangeEventHandler, FormEventHandler } from "react"

interface Props{
    isOpen: boolean,
    onClose: Function,
    formData: {chat_name: string, context: string},
    handleChatChangeSubmit: FormEventHandler<HTMLFormElement>,
    handleChatChangeFormChange: ChangeEventHandler<HTMLTextAreaElement|HTMLInputElement>
}

export default function ChatSettings({
    isOpen, onClose, formData, handleChatChangeSubmit, handleChatChangeFormChange}: Props) {
    if (!isOpen) {return null}
    
    return (
        <div className={styles.container}>
            <div className={styles.headingContainer}>
                <h2>Change Chat Settings</h2>
                <button className={styles.closeButton} onClick={() => onClose()}>
                    X
                </button>
            </div>
            <form onSubmit={handleChatChangeSubmit} className={styles.form}>
                    <div className={styles.inputContainer}>
                        <label className={styles.changeLabel}>Chat Name</label>
                        <input 
                            name="chat_name"
                            type="text"
                            className={styles.changeChatInput}
                            value={formData?.chat_name}
                            onChange={handleChatChangeFormChange}
                            required/>
                    </div>
                    <div className={styles.inputContainer}>
                        <label className={styles.changeLabel}>Context</label>
                        <textarea 
                            name="context"
                            className={styles.changeChatInput}
                            onChange={handleChatChangeFormChange}
                            value={formData?.context}
                            rows={5}
                            cols={40}/>
                    </div>
                    <button type="submit" className={styles.submitChangeButton}>Submit changes</button>
                </form>
        </div>
    )
}
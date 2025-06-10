import styles from './chatInput.module.css'

export default function ChatInput({
    handleSendMessage,
    currentMessage,
    setCurrentMessage
}: {
    handleSendMessage: Function,
    currentMessage: string,
    setCurrentMessage: Function
}) {
    return (
        <div className={styles.inputContainer}>
            <input 
                className={styles.input}
                onChange={(event) => setCurrentMessage(event.target.value)} 
                value={currentMessage} 
            />
            <button 
                className={styles.button}
                onClick={() => handleSendMessage()}
                >
                Send
            </button>
        </ div>
    )
}

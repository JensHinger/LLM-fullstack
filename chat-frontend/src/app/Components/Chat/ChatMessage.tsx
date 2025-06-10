import IMessage from "@/Models/IMessage"
import styles from "./chatMessage.module.css"


export default function ChatMessage(
    {messageProps}:{messageProps: IMessage}
){
    // Style should be based on role either left or right bound and color should differ

    var messageStyling = messageProps.author == "user"? styles.userMessage : styles.agentMessage
    return (
        <div className={`${messageStyling} ${styles.message}`}>
            {messageProps.text}
        </div>
    )
}
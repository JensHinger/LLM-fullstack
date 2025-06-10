import Chat from "@/Models/IChat";
import styles from "./createChatForm.module.css"
import { routeToChat } from "@/utils/routing";

export default function CreateChatForm(){
    async function createChat(formData: FormData) {
        "use server"
        const formChatName = formData.get("chatName");

        if (formChatName){ 
            const res = await fetch("http://localhost:3000/api/chat", 
                {
                    method: "POST",
                    body: JSON.stringify({
                        chatName: formChatName
                    })
                }
            )

            const chat: Chat = await res.json()
            
            // After chat creation should reload chat sidebar and navigate to the new chat
            routeToChat(chat)
        }
    }

    return (
        <div className={styles.formContainer}>
            <p className={styles.info}>To create a new Chat enter a name:</p>
            <form className={styles.form} action={createChat}>
                
                <input className={styles.input} name="chatName" placeholder="New Chat" />
                <button className={styles.button} type="submit">Create New Chat</button>
            </form>
        </ div>
    )
}
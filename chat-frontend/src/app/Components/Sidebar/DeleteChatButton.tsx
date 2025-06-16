'use client'

import { usePathname, useRouter } from "next/navigation";
import styles from "./deleteChatButton.module.css"

interface Props {
    chatId: string;
}

export default function DeleteChatButton({ chatId } : Props) {
    const pathname = usePathname();
    const router = useRouter();   

    const handleDelete = async () => {
        const res = await fetch(`/api/chat/${chatId}`, {
            method: "DELETE",
        });

        if (res.ok) {
            const isOpenChat = pathname.slice(6) == chatId;

            if(isOpenChat) {
                router.replace("/");
            }
            
            router.refresh();
        } else {
            console.error("Failed to delete chat")
        }

    }

    return <button onClick={handleDelete} className={styles.deleteChat}>X</button>
}
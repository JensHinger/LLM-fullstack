import Chat from "@/Models/IChat"
import { redirect } from "next/navigation"

export function routeToChat(chat: Chat){
    redirect(`/chat/${chat.chat_id}?chatName=${chat.chat_name}&context=${chat.context}&llmModel=${chat.llm_model}`)
}
import Chat from "@/app/Components/Chat/Chat";
import IChat from "@/Models/IChat";

interface chatParams{
    params: Promise<{chat_id:string}>,
    searchParams: Promise<{ [key: string ]: string | undefined}>
}


export default async function Page(chatParams: chatParams) {

    const { chat_id } = await chatParams.params;
    const { chatName, context, llmModel } = await chatParams.searchParams;

    const chat: IChat = {
        chat_id: parseInt(chat_id),
        chat_name: chatName? chatName : "",
        context: context? context : "",
        llm_model: llmModel? llmModel : ""
    }

    return (
        <Chat chat={chat} />
    );
}

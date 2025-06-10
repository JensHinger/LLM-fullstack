import Chat from "@/app/Components/Chat/Chat"

const context_api_url = "/api/v1/chats" 

export async function GET(request: Request){
    const res = await fetch(process.env.API_URL + context_api_url, {method:"GET"})
    const data = await res.json()
    return Response.json(data)
}

export async function POST(request: Request){
    const newChatName = (await request.json()).chatName

    const res = await fetch(process.env.API_URL + context_api_url,{
        method: "POST",
         headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            chatName: newChatName,
        })
    })
    return Response.json(await res.json())
}
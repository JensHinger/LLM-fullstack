import Message from "@/Models/IMessage"

const context_api_url = "/api/v1/messages" 

export async function GET(
    request: Request,
    {params}: {params: Promise<{chatID: string}>}
){
    const { chatID } = await params

    const res = await fetch(process.env.API_URL + context_api_url + "/" + chatID, {method:"GET"})
    const data = await res.json()
    return Response.json(data)
}

export async function POST(
    request: Request,
    {params}: {params: Promise<{chatID: string}>}
){
    const message = (await request.json())
    const { chatID } = await params

    const res = await fetch(process.env.API_URL + context_api_url + "/" + chatID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }, 
        body: JSON.stringify(message)
    })
    const data = await res.json()
    return Response.json(data)
}
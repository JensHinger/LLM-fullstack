const context_api_url = "/api/v1/chat" 

// Currently unused
export async function GET(
    request: Request,
    {params}: {params: Promise<{chatID: string}>}
){
    const chatID = (await params).chatID

    const res = await fetch(process.env.API_URL + context_api_url + "/" + chatID, {method:"GET"})
    const data = await res.json()
    return Response.json(data)
}
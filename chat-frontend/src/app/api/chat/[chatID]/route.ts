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

export async function DELETE(
    request: Request,
    {params}: {params: Promise<{chatID: string}>}
) {
    const chatID = (await params).chatID;

    await fetch(process.env.API_URL + context_api_url + "/" + chatID, {method:"DELETE"})
    return Response.json({ "message": "Chat deleted successfully!"})
}

export async function PUT(
    request: Request,
    {params}: {params: Promise<{chatID: string}>}
) {
    const chatID = (await params).chatID;
    const payload = await request.json()
    const res = await fetch(process.env.API_URL + context_api_url + "/" + chatID, {
        method:"PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload)
    })

    return Response.json(await res.json())
}
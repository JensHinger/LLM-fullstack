import { NextResponse } from "next/server";

const context_api_url = "/api/v1/chats" 

export async function POST(request: Request) {
    const res = await fetch(process.env.API_URL + context_api_url, {method:"DELETE"})
    return res
}
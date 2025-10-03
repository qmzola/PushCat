from fastapi import FastAPI, Request,HTTPException
import asyncio

app = FastAPI()

TOKEN = "test123"


@app.post("/webhook/client/{token}")
async def webhook(token:str,request: Request, payload: dict):
    if TOKEN != token:
        raise HTTPException(status_code=401, detail="Invalid token")
    # payload 是自动解析的 JSON
    # request 可用于获取原始信息（如 headers、IP 等）
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    input_queue.put(payload)
    return {"status": "Created"}, 201

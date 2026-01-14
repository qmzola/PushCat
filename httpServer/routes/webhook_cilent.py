from typing import List, Literal
from fastapi import FastAPI, APIRouter,status
from starlette.responses import JSONResponse
from pydantic import BaseModel
from ConfigRead.ConfigReader import load_config
from msgedit import msgPrint

config=load_config()

class MessageBody(BaseModel):
    type: Literal["text"]
    title: str
    body: str

class Message(BaseModel):
    type: Literal["text"]
    content: List[MessageBody]

class WebhookRequest(BaseModel):
    sender: str
    time: str  # 通常为 ISO 8601 格式的时间字符串，如 "2026-01-14T10:00:00Z"
    token: str
    platform: List[str]  # 或更严格地用 Literal["DingTalk", ...] 如果平台固定
    message: Message



router=APIRouter(
    prefix="/webhook",
    tags=["webhook client"],
)

@router.post("/{url_keys}", tags=["webhook"])
async def webhook(url_keys: str,webhook_request: WebhookRequest):
    if url_keys !=config.input_token.url_access_token :
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Unauthorized", "message": "Invalid URL token"}
        )
    if webhook_request.token != config.input_token.input_access_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Unauthorized", "message": "Invalid URL token"}
        )
    else:
        msgPrint.msg_print(webhook_request)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Success"}
        )
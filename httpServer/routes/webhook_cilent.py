from typing import List, Literal
from fastapi import FastAPI, APIRouter,status
from starlette.responses import JSONResponse
from pydantic import BaseModel
from ConfigRead.ConfigReader import load_config
from msgedit import msgPrint
from app_logging import get_logger

logger = get_logger("WebhookRequest")
config=load_config()

#消息规整化
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


#消息请求端点信息
router=APIRouter(
    prefix="/webhook",
    tags=["webhook client"],
)
#消息请求处理
@router.post("/{url_keys}", tags=["webhook"])
async def webhook(url_keys: str,webhook_request: WebhookRequest):
    if url_keys !=config.input_token.url_access_token :
        logger.warning(f"消息请求路径不正确")
        logger.debug(f"此请求的请求地址为/api/v1/webhook/{url_keys}，但是实际地址为{config.input_token.url_access_token}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Unauthorized", "message": "Invalid URL token"}
        )
    if webhook_request.token != config.input_token.input_access_token:
        logger.warning("消息体内Token不正确")
        logger.debug(f"消息体内token为{config.input_token.input_access_token}，于配置文件中的不符")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Unauthorized", "message": "Invalid URL token"}
        )
    else:
        msgPrint.msg_print(webhook_request)
        logger.info(f"接收到一条来自api/v1/webhook的请求{url_keys}。已被正确接收")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Success"}
        )
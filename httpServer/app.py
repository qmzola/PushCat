from fastapi import FastAPI
from ConfigRead.ConfigReader import load_config

config = load_config()

#配置全局路径
api = FastAPI(
    root_path="/api",
    docs_url="/docs" if config.debug.api_docs else None,
    openapi_url="/openapi.json" if config.debug.api_docs else None,
    redoc_url="/redoc" if config.debug.api_docs else None,
)

#引入具体请求处理模块
from .routes import webhook_cilent

api.include_router(webhook_cilent.router, prefix="/v1", tags=["Webhook client"])
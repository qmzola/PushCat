from fastapi import FastAPI
from ConfigRead.ConfigReader import load_config

config = load_config()

api = FastAPI(
    root_path="/api",
    docs_url="/docs" if config.debug.api_docs else None,
    openapi_url="/openapi.json" if config.debug.api_docs else None,
    redoc_url="/redoc" if config.debug.api_docs else None,
)

from .routes import webhook_cilent

api.include_router(webhook_cilent.router, prefix="/v1", tags=["Webhook client"])
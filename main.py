import logging
import queue
import asyncio
import httpServer
import app_logging

httpServer.start_http_server()

"""if __name__ == "__main__":
   import uvicorn
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)"""
import logging
import queue
import asyncio
import httpServer
import sys
from app_logging import get_logger
from ConfigRead.ConfigReader import load_config
import uvicorn


logger = get_logger("start")
config = load_config()
host_str=str(config.server.host)

#对两项高危操作进行二次确认

#对debug模式进行二次确认
logger.info(f"config.debug.debug_mode值为{config.debug.debug_mode}")
if config.debug.debug_mode==True:
    debug_mode_confirmation=input("你已经在配置文件中开启了调试模式，请进行二次确认。如要开启调试模式请输入Yes i do")
    if debug_mode_confirmation != "Yes i do" :
        logger.error("请调整配置文件中的debug选项来关闭debug模式。配置文件在Configs/config.toml")
        sys.exit(1)
    else:
        logger.warning("已开启调试模式。调试模式可能降低安全性以及性能。以及可能导致意外的信息泄漏。用完及时关闭")

#对api docs的展示进行二次确认
if config.debug.api_docs == True:
    api_docs_confirmation=input("你已在配置文件中开启了展示api文档，请进行二次确认。如要对外展示api文档请输入Yes")
    if api_docs_confirmation != "Yes" :
        logger.error("请调整配置文件中的api_docs选项来关闭api文档对外展示。配置文件在Configs/config.toml")
        sys.exit(1)
    else:
        logger.warning("已开启对外展示api文档。对外展示api文档会暴露api端点信息以及api的调用方法等。会降低安全性。用后请及时关闭")



if __name__ == "__main__":
    uvicorn.run(
        httpServer.app.api,
        host=host_str,
        port=config.server.port,
        reload= config.debug.debug_mode,
        workers=1,
    )

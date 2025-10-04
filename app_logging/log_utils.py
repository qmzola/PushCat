
"""
log_util.py
一个极简、零依赖（仅用标准库）的日志工具。
特性：
  1) 控制台实时打印
  2) 按日期分文件存储
  3) 统一格式：时间 - 等级 - 模块 - 消息
"""
import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
import tomllib

_LOG_INITIALIZED = False  # 单例标记


def setup_logging(
    log_dir: Path | str = "logs",
    console_level: int | str = "INFO",
    file_level: int | str = "DEBUG",
    retention_days: int = 30,
):
    """保证整个进程只初始化一次"""
    global _LOG_INITIALIZED
    if _LOG_INITIALIZED:
        return

    log_dir = Path(log_dir)
    log_dir.mkdir(mode=0o750, parents=True, exist_ok=True)

    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    # ---------- 控制台 ----------
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(console_level)
    console.setFormatter(formatter)

    # ---------- 文件（按日期滚动） ----------
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_dir / f"{datetime.now():%Y-%m-%d}.log",
        when="midnight",  # 每天 0 点切分
        interval=1,
        backupCount=retention_days,
        encoding="utf-8",
        delay=False,
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # ---------- 根日志器 ----------
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # 全局最低
    root.addHandler(console)
    root.addHandler(file_handler)

    _LOG_INITIALIZED = True


def get_logger(name: str | None = None) -> logging.Logger:
    """
    获取日志器。
    传入 __name__ 即可：logger = get_logger(__name__)
    """
    if not _LOG_INITIALIZED:
        # 如果没有初始化，使用默认配置
        setup_logging()
    return logging.getLogger(name)


# ------------------ demo ------------------
if __name__ == "__main__":
    # 从配置文件加载日志配置
    try:
        with open("configs/config.toml", "rb") as f:
            config = tomllib.load(f).get("Logging", {})
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        config = {}

    # 初始化日志
    setup_logging(
        log_dir=config.get("log_dir", "logs"),
        console_level=config.get("console_level", "INFO"),
        file_level=config.get("file_level", "DEBUG"),
        retention_days=config.get("retention_days", 30),
    )

    logger = get_logger(__name__)
    logger.debug("这是 debug")
    logger.info("这是 info")
    logger.warning("这是 warning")
    logger.error("这是 error")


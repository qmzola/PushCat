import tomllib
from .log_utils import setup_logging, get_logger
from pydantic import BaseModel,ValidationError
from enum import Enum


# 配置配置文件校验模型
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig(BaseModel):
    log_dir: str = "logs"
    console_level: LogLevel = LogLevel.INFO
    file_level: LogLevel = LogLevel.DEBUG
    retention_days: int = 30


# 从配置文件加载日志配置
from pathlib import Path

config_path = Path("configs/config.toml")
try:
    if config_path.exists():
        with open(config_path, "rb") as f:
            config = tomllib.load(f).get("Logging", {})
    else:
        config = {}
except (FileNotFoundError, tomllib.TOMLDecodeError, OSError):
    config = {}

# 使用 LoggingConfig 模型验证配置
try:
    logging_config = LoggingConfig(**config)
except ValidationError as e:
    raise RuntimeError("日志配置无效") from e

# 初始化日志
setup_logging(
    log_dir=logging_config.log_dir,
    console_level=logging_config.console_level.value,
    file_level=logging_config.file_level.value,
    retention_days=logging_config.retention_days,
)

# 暴露 get_logger 函数
__all__ = ["get_logger"]

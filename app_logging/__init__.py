import tomllib
from .log_utils import setup_logging, get_logger
from pydantic import BaseModel
from enum import Enum
from pydantic import ValidationError


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
try:
    with open("configs/config.toml", "rb") as f:
        config = tomllib.load(f).get("Logging", {})
except (FileNotFoundError, tomllib.TOMLDecodeError):
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

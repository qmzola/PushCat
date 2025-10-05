from pathlib import Path
from typing import Optional
from pydantic import BaseModel, model_validator
import tomllib
import logging
from app_logging import logging_config, get_logger
import shutil
import secrets

logger = get_logger("ConfigReader")

class Users(BaseModel):
    user_url: str
    user_id: int
    user_name: str

# 对读取到的ingTalk相关配置选项进行格式判断
class DingTalk(BaseModel):
    enabled: bool = False
    access_token: Optional[str] = None
    secret: Optional[str] = None

# 处理为关时或开时缺少token/secret的情况
    @model_validator(mode='after')
    def validate_token_if_enabled(self):
        if self.enabled:
            missing=[]
            if not self.access_token or not self.access_token.strip():
                missing.append("token")
            if not self.secret or not self.secret.strip():
                missing.append("secret")
            if missing:
                logging.error(f"钉钉平台{', '.join(missing)}未配置，功能将被禁用。")
                self.enabled = False
        return self

from pydantic import Field

class InputToken(BaseModel):
    input_access_token: str

# 主配置模型
class Config(BaseModel):
    user: Users
    dingtalk: DingTalk
    input_token: InputToken


# 读取toml文件
config_dir = Path("configs")
current_dir = Path(__file__).parent
config_template_file = current_dir / "config_template.toml"

def load_config(toml_file_path: str = str(Path("configs") / "config.toml")) -> Config:
    config_path = Path(toml_file_path)
    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
            mapped_data = {
                "user": data.get("Users"),
                "dingtalk": data.get("DingTalk"),
                "input_token": data.get("InputToken")
            }
            return Config.model_validate(mapped_data)
    except (FileNotFoundError, PermissionError):  # 处理文件不存在或目录不存在的情况
        logger.warning("未读取到配置文件，即将创建配置文件。")
        config_path.parent.mkdir(exist_ok=True)
        with open(config_template_file, 'r', encoding='utf-8') as template_file:
            template_content = template_file.read()
        generated_token = secrets.token_hex()
        logger.info(f"你的InputToken为{generated_token}")
        updated_content = template_content.replace('input_access_token=""', f'input_access_token="{generated_token}"')
        with open(config_path, 'w', encoding='utf-8') as new_config:
            new_config.write(updated_content)
        with open(config_path, "rb") as f:#重新读取配置文件
            data = tomllib.load(f)
            mapped_data = {
                "user": data.get("Users"),
                "dingtalk": data.get("DingTalk"),
                "input_token": data.get("InputToken")
            }
            return Config.model_validate(mapped_data)
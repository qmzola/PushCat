ky import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, model_validator
import tomllib


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
                logging.ERROR(f"钉钉平台{', '.join(missing)}未配置，功能将被禁用。")
                self.enabled = False
        return self

# 主配置模型
class Config(BaseModel):
    user: Users
    dingtalk: DingTalk

# 读取toml文件
def load_config(toml_file_path: str = "configs/config.toml") -> Config:
    with open(toml_file_path, "rb") as f:
        data = tomllib.load(f)
        mapped_data = {
            "user": data.get("Users"),
            "dingtalk": data.get("DingTalk")
        }
        return Config.model_validate(mapped_data)
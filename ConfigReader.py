import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, model_validator
import tomllib


class Users(BaseModel):
    user_url: str
    user_id: int
    user_name: str

# 读取钉钉的配置文件
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


class Config(BaseModel):
    """
    主配置模型
    """
    user: Users
    dingtalk: DingTalk


def load_config(toml_file_path: str = "configs/config.toml") -> Config:
    with open(toml_file_path, "rb") as f:
        data = tomllib.load(f)
        # Map the keys from the TOML file to the pydantic model fields
        mapped_data = {
            "user": data.get("Users"),
            "dingtalk": data.get("DingTalk")
        }
        return Config.model_validate(mapped_data)


if __name__ == "__main__":
    cfg = Users()
    print(f"用户名：{cfg.user.name}，钉钉token：{cfg.dingtalk.webhook}")

"""

def load_config(toml_file: str = "config/config.toml") -> Config:
    
    # 从 TOML 文件加载配置
    # 路径基于当前文件所在目录（config.py 所在目录）
    
    # 获取当前文件所在目录
    current_dir = Path(__file__).parent
    toml_path = current_dir / toml_file  # 假设 config.toml 在 config/ 子目录中

    try:
        with open(toml_path, "rb") as f:
            toml_data = tomllib.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件 {toml_path} 未找到")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"配置文件格式错误: {e}")

    try:
        config = Config(**toml_data)
        print(f"✅ 配置加载成功: {toml_path}")
        return config
    except Exception as e:
        raise ValueError(f"配置验证失败: {e}")




"""

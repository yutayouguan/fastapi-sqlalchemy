"""
Author: 王猛
Date: 2024-05-10 19:12:33
LastEditors: damon wang
LastEditTime: 2024-05-15 10:18:54
FilePath: /fastapi-project/src/config.py
Description:全局配置 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path

DESCRIPTION = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""


class ContactConfig(BaseModel):
    """API 联系信息"""

    name: str = "damon wang"
    url: str = "https://github.com/damonwang"
    email: str = "damonwang@gmail.com"


class LicenseConfig(BaseModel):
    """许可证信息"""

    name: str = "MIT"
    url: str = "https://opensource.org/licenses/MIT"


class APPConfig(BaseModel):
    """App 配置"""

    debug: bool = False
    name: str = "FastAPI 项目"
    description: str = DESCRIPTION
    summary: str = "一个使用 FastAPI 构建的示例项目"
    version: str = "0.0.1"
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"
    root_path: str = ""
    terms_of_service: str = "https://github.com/damonwang"
    contact: ContactConfig = ContactConfig()
    license_info: LicenseConfig = LicenseConfig()


class PGConfig(BaseModel):
    """PostgreSQL数据库配置"""

    host: str = "localhost"
    port: int = 5432
    user: str = "root"
    password: str = "123456"
    database: str = "fastapi_project"


class MySQLConfig(BaseModel):
    """MySQL数据库配置"""

    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "123456"
    database: str = "fastapi_project"


class CORSConfig(BaseModel):
    """跨域资源共享配置"""

    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]
    expose_headers: list[str] = [
        "X-Process-Time",
    ]
    max_age: int = 600


class ServerConfig(BaseModel):
    """服务器配置"""

    host: str = "0.0.0.0"
    port: int = 8000
    project_root: Path = Path(__file__).parent.parent
    base_dir: Path = project_root.parent
    log_dir: Path = base_dir / "logs"


class Settings(BaseSettings):
    """全局配置"""

    # App 配置
    app: APPConfig = APPConfig()
    # 服务器配置
    server: ServerConfig = ServerConfig()
    # 数据库配置
    # db: PGConfig = PGConfig()
    db: MySQLConfig = MySQLConfig()
    SQLALCHEMY_DATABASE_URL: str = (
        f"mysql+pymysql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}"
    )
    # 跨域资源共享配置
    cors: CORSConfig = CORSConfig()

    model_config = SettingsConfigDict(
        env_file=".env",  # 环境变量文件路径
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # 嵌套环境变量分隔符
        env_prefix="app_",  # 环境变量前缀
        case_sensitive=True,  # 忽略大小写
    )


@lru_cache
def get_settings() -> Settings:
    """获取全局配置"""
    return Settings()


settings = get_settings()

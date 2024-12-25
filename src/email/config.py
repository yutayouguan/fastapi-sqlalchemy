"""
Author: 王猛
Date: 2024-05-17 22:53:59
LastEditors: 王猛
LastEditTime: 2024-05-18 01:51:03
FilePath: /fastapi-project/src/email/config.py
Description: 邮箱配置信息

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class _Settings(BaseSettings):

    # 邮件配置
    SMTP_SERVER: str = "smtp.qq.com"
    SMTP_PORT: int = 587  # 端口 465 用于 SSL/TLS 连接，端口 587 用于 STARTTLS 连接
    SMTP_USERNAME: str = "2525453626@qq.com"
    SMTP_PASSWORD: str = "vmoprqkxrjliebac"  # 替换为实际的QQ邮箱授权码或密码
    SMTP_FROM: EmailStr = "2525453626@qq.com"

    model_config = SettingsConfigDict(env_file=".env")


settings = _Settings()

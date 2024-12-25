"""
Author: 王猛
Date: 2024-05-17 22:54:47
LastEditors: 王猛
LastEditTime: 2024-05-18 02:31:38
FilePath: /fastapi-project/src/email/router.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from tempfile import gettempdir
from anyio import Path
from fastapi import APIRouter, Form, Response, UploadFile, status, File
from pydantic import EmailStr
from .utils import send_email_with_attachment
from src.utils import logger

router = APIRouter()


@router.post("/send-email/")
async def send_email(
    subject: str = Form(..., description="邮件主题", examples=["注册邮件"]),
    body: str = Form(..., description="邮件正文", examples=["欢迎注册我们的网站"]),
    to_emails: list[EmailStr] = Form(
        ..., description="收件人邮箱地址", examples=["user@example.com"]
    ),
    attachment_files: list[UploadFile] = File(
        None, description="附件文件", examples=["attachment.pdf"]
    ),
):
    attachment_paths: list[Path] = []  # 存储附件的路径
    if attachment_files:
        for file in attachment_files:
            file_location = Path(f"{gettempdir()}/{file.filename}")  # 创建临时文件路径
            await file_location.write_bytes(await file.read())  # 将附件保存到本地
            attachment_paths.append(file_location)

    # 发送邮件
    await send_email_with_attachment(subject, body, to_emails, attachment_paths)
    for file_path in attachment_paths:
        await file_path.unlink()  # 删除临时文件
    return "Email sent successfully"


@router.post("/send-email-bg/")
async def send_email_bg(
    subject: str = Form(..., description="邮件主题", examples=["注册邮件"]),
    body: str = Form(..., description="邮件正文", examples=["欢迎注册我们的网站"]),
    to_emails: list[EmailStr] = Form(
        ..., description="收件人邮箱地址", examples=["user@example.com"]
    ),
    attachment_files: list[UploadFile] = File(
        None, description="附件文件", examples=["attachment.pdf"]
    ),
):
    
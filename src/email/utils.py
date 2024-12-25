"""
Author: 王猛
Date: 2024-05-17 22:54:20
LastEditors: 王猛
LastEditTime: 2024-05-18 02:27:14
FilePath: /fastapi-project/src/email/utils.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from pydantic import EmailStr
from .config import settings
from anyio import Path
from loguru import logger


async def send_email_with_attachment(
    subject: str,
    body: str,
    to_emails: list[EmailStr],
    attachments: list[Path] | None = None,
):
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    msg.attach(payload=MIMEText(_text=body, _subtype="plain", _charset="utf-8"))

    if attachments:
        for attachment in attachments:
            attachment_mime = MIMEApplication(await attachment.read_bytes())
            attachment_mime.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment.name,
            )  # 设置附件名称
            msg.attach(payload=attachment_mime)  # 添加附件

    try:
        async with aiosmtplib.SMTP(
            hostname=settings.SMTP_SERVER, port=settings.SMTP_PORT
        ) as smtp:
            await smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            await smtp.send_message(msg)

        logger.info(f"邮件发送成功，收件人：{to_emails}")
    except Exception as e:
        logger.exception(f"邮件发送失败，收件人：{to_emails}，原因：{e}")

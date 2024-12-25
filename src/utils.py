"""
Author: damon wang
Date: 2024-05-15 10:15:26
LastEditors: 王猛
LastEditTime: 2024-05-18 00:13:05
FilePath: /fastapi-project/src/utils.py
Description: 

Copyright (c) 2024 by damon wang wmdyx@outlook.com, All Rights Reserved. 
"""

from functools import lru_cache
import sys
from loguru import logger
from .config import settings


class Logger:
    def __init__(self) -> None:
        self.level = ["INFO", "DEBUG"][bool(settings.app.debug)]
        logger.remove()

    @lru_cache
    def setup(self):
        # 日志配置
        log_config = {
            "handlers": [
                {
                    "sink": settings.server.log_dir
                    / settings.app.name
                    / f"{settings.app.name}.log",
                    "level": self.level,
                },
                {
                    "sink": settings.server.log_dir
                    / settings.app.name
                    / f"{settings.app.name}_error.log",
                    "level": "ERROR",
                },
                {"sink": sys.stdout, "level": self.level},
            ],
            "extra": {
                "format": "{time:YYYY-MM-DD at HH:mm:ss} {level}- {message}",
                #  "format" : " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}",
                "enqueue": True,
                "rotation": "10 MB",
                "retention": "10 days",
                "compression": "zip",
            },
        }
        logger.configure(**log_config)
        return logger


logger = Logger().setup()

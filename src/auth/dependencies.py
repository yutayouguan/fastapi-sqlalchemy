"""
Author: 王猛
Date: 2024-05-10 19:31:01
LastEditors: 王猛
LastEditTime: 2024-12-25 09:39:40
FilePath: /fastapi-project/src/auth/dependencies.py
Description: 路由依赖(Depends)

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

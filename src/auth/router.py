"""
Author: 王猛
Date: 2024-05-10 19:30:32
LastEditors: 王猛
LastEditTime: 2024-05-18 00:05:22
FilePath: /fastapi-project/src/auth/router.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

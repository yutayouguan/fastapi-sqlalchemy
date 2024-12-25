"""
Author: 王猛
Date: 2024-05-11 10:41:11
LastEditors: damon wang
LastEditTime: 2024-05-15 09:36:29
FilePath: /fastapi-project/src/dependencies.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from fastapi import Depends

from src.models import User
from .database import get_db, Session
from fastapi import HTTPException
from .crud import get_user


def get_current_user(db: Session = Depends(get_db)):
    return get_user(db, 1)


def get_current_active_user(db: Session = Depends(get_db)):
    user: User | None = get_current_user(db)
    if user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return user


def get_current_active_superuser(db: Session = Depends(get_db)):
    user: User = get_current_active_user(db)
    if not user.is_superuser:  # type: ignore
        raise HTTPException(status_code=403, detail="Not superuser")
    return user


def get_current_active_superuser_or_admin(db: Session = Depends(get_db)):
    user: User = get_current_active_user(db)
    if not user.is_superuser and not user.is_admin:  # type: ignore
        raise HTTPException(status_code=403, detail="Not superuser or admin")
    return user

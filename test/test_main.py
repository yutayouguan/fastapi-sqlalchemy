"""
Author: 王猛
Date: 2024-05-12 22:28:27
LastEditors: 王猛
LastEditTime: 2024-05-12 22:44:52
FilePath: /fastapi-project/test/test_main.py
Description: 

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

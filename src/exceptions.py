import json
from fastapi import FastAPI, Request, Response, WebSocket, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
    ResponseValidationError,
    WebSocketRequestValidationError,
)
from fastapi.responses import JSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from tortoise.exceptions import (
    DoesNotExist,
    IntegrityError,
    ValidationError,
    FieldError,
)
from pydantic_core import ValidationError as pydantic_ValidationError
from .utils import logger
from json.decoder import JSONDecodeError
from aiosmtplib.errors import SMTPConnectError


class SettingNotFound(Exception):
    """Raised when a setting is not found"""

    ...


async def smtp_connect_error_handler(
    request: Request, exc: SMTPConnectError
) -> JSONResponse:
    """处理SMTP连接错误"""
    content = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    return JSONResponse(
        content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """处理HTTP请求错误"""
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    content = {
        "code": exc.status_code,
        "detail": exc.detail,
        "type": exc.__class__.__name__,
    }
    return JSONResponse(content=content, status_code=exc.status_code, headers=headers)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """处理数据验证错误"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": jsonable_encoder(exc.errors()),
            "type": "RequestValidationError",
        },
    )


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    """处理WebSocket错误"""
    logger.exception(exc)
    await websocket.close(
        code=status.WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
    )


async def json_decode_error_handler(
    request: Request, exc: JSONDecodeError
) -> JSONResponse:
    """处理 json 解码错误"""
    content = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content
    )


async def field_error_handler(request: Request, exc: FieldError) -> JSONResponse:
    """数据库字段异常处理"""
    content = {
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content
    )


async def does_not_exist_handler(request: Request, exc: DoesNotExist) -> JSONResponse:
    """处理数据库对象不存在DoesNotExist异常"""
    content = {
        "code": status.HTTP_404_NOT_FOUND,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)


async def integrity_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    """处理数据库完整性错误 IntegrityError"""
    content = {
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content
    )


async def model_validation_error_handler(
    _: Request, exc: ValidationError
) -> JSONResponse:
    """处理ORM验证错误"""
    content = {
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content
    )


async def request_validation_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    """处理请求验证错误"""
    content = {
        "code": status.HTTP_400_BAD_REQUEST,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(content=content, status_code=status.HTTP_400_BAD_REQUEST)


async def response_validation_handler(
    _: Request, exc: ResponseValidationError
) -> JSONResponse:
    """处理响应验证错误"""
    content = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": jsonable_encoder(exc),
        "type": exc.__class__.__name__,
    }
    logger.exception(content)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content
    )


async def validation_error_handler(_: Request, exc: pydantic_ValidationError):
    """处理模型验证错误"""
    content = {
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": exc.json(indent=4),
        "type": exc.__class__.__name__,
    }
    content["msg"] = json.loads(content["detail"]["msg"])
    logger.exception(content)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DoesNotExist, does_not_exist_handler)  # type: ignore
    app.add_exception_handler(IntegrityError, integrity_handler)  # type: ignore
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore
    app.add_exception_handler(ResponseValidationError, response_validation_handler)  # type: ignore
    app.add_exception_handler(WebSocketRequestValidationError, websocket_request_validation_exception_handler)  # type: ignore
    app.add_exception_handler(pydantic_ValidationError, validation_error_handler)  # type: ignore
    app.add_exception_handler(ValidationError, model_validation_error_handler)  # type: ignore
    app.add_exception_handler(JSONDecodeError, json_decode_error_handler)  # type: ignore
    app.add_exception_handler(FieldError, field_error_handler)  # type:ignore

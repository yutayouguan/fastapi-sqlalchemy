from typing import Generic, TypeVar
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class CRUDBase(Generic[ModelType]): ...

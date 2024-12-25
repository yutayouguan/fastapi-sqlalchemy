"""
Author: 王猛
Date: 2024-05-10 19:30:48
LastEditors: 王猛
LastEditTime: 2024-05-18 15:25:10
FilePath: /fastapi-project/src/auth/models.py
Description: ORM 模型或者数据库表定义文件

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
"""

from sqlalchemy import Enum
from sqlalchemy import Index
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declared_attr
from enum import Enum as PyEnum


class StatusEnum(PyEnum):
    FROZEN = 0
    ACTIVE = 1
    DELETED = 2


class RequestMethodEnum(PyEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class MenuTypeEnum(PyEnum):
    CATALOG = "CATALOG"
    MENU = "MENU"


class OperationTypeEnum(PyEnum):
    ADD = "ADD"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class PermissionTypeEnum(PyEnum):
    MENU = "MENU"
    API = "API"


class ObjectTypeEnum(PyEnum):
    DEPARTMENT = "DEPARTMENT"
    ROLE = "ROLE"
    USER = "USER"
    MENU = "MENU"
    API = "API"
    PERMISSION = "PERMISSION"
    MODULE = "MODULE"
    USER_ROLE = "USER_ROLE"
    ROLE_PERMISSION = "ROLE_PERMISSION"
    USER_DEPARTMENT = "USER_DEPARTMENT"


class BaseMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), comment="创建时间")

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime, default=func.now(), onupdate=func.now(), comment="更新时间"
        )

    @declared_attr
    def created_by(cls):
        return Column(String(50), comment="创建者")

    @declared_attr
    def updated_by(cls):
        return Column(String(50), comment="更新者")

    @declared_attr
    def last_updated_ip(cls):
        return Column(String(45), comment="最后一次更新者的IP")


class Base(DeclarativeBase):
    __abstract__ = True


class User(Base, BaseMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), nullable=False, comment="用户名")
    employee_num = Column(String(50), unique=True, nullable=False, comment="工号")
    password_hash = Column(String(255), nullable=False, comment="密码哈希值")
    email = Column(String(100), comment="邮箱")
    department_id = Column(
        Integer, ForeignKey("departments.department_id"), comment="部门ID"
    )
    is_active = Column(Boolean, default=True, comment="是否激活")
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, comment="状态")
    is_admin = Column(Boolean, default=False, comment="是否管理员")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    last_login_time = Column(DateTime, comment="最后一次登录时间")
    login_count = Column(Integer, default=0, comment="登录次数")

    department = relationship("Department", back_populates="users")
    roles = relationship("Role", secondary="user_roles", back_populates="users")


Index("idx_username", User.username)
Index("idx_email", User.email)
Index("idx_employee_num", User.employee_num)
Index("idx_department_id", User.department_id)


class Department(Base, BaseMixin):
    __tablename__ = "departments"
    department_id = Column(
        Integer, primary_key=True, autoincrement=True, comment="部门ID"
    )
    department_name = Column(String(50), nullable=False, comment="部门名称")
    parent_department_id = Column(
        Integer, ForeignKey("departments.department_id"), comment="父级部门ID"
    )
    department_level = Column(Integer, default=1, comment="部门层级")
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, comment="状态")
    order = Column(Integer, default=0, comment="排序")

    users = relationship("User", back_populates="department")
    children = relationship(
        "Department", back_populates="parent", cascade="all, delete-orphan"
    )
    parent = relationship(
        "Department", remote_side=[department_id], back_populates="children"
    )


Index("idx_department_name", Department.department_name)
Index("idx_department_level", Department.department_level)
Index("idex_department_status", Department.status)


class Role(Base, BaseMixin):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=True, comment="角色ID")
    role_name = Column(String(50), nullable=False, unique=True, comment="角色名称")
    role_type = Column(String(50), nullable=False, comment="角色类型")
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, comment="状态")

    user_roles = relationship("UserRole", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")
    users = relationship("User", secondary="user_roles", back_populates="roles")


Index("idx_role_name", Role.role_name)
Index("idx_role_type", Role.role_type)
Index("idx_role_status", Role.status)


class Permission(Base, BaseMixin):
    __tablename__ = "permissions"
    permission_id = Column(
        Integer, primary_key=True, autoincrement=True, comment="权限ID"
    )
    permission_code = Column(
        String(50), nullable=False, unique=True, comment="权限代码"
    )
    permission_name = Column(
        String(100), nullable=False, unique=True, comment="权限名称"
    )
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, comment="状态")
    permission_path = Column(String(200), nullable=False, comment="权限路径")
    permission_type = Column(String(50), nullable=False, comment="权限类型")
    parent_permission_id = Column(
        Integer, ForeignKey("permissions.permission_id"), comment="父级权限ID"
    )
    source_type = Column(String(50), nullable=False, comment="数据源类型")
    permission_level = Column(Integer, default=1, comment="权限层级")
    order = Column(Integer, default=0, comment="排序")

    parent_permission = relationship(
        "Permission", remote_side=[permission_id], back_populates="children_permission"
    )
    children_permission = relationship(
        "Permission", back_populates="parent_permission", cascade="all, delete-orphan"
    )


Index("idx_permission_code", Permission.permission_code)
Index("idx_permission_name", Permission.permission_name)
Index("idx_permission_type", Permission.permission_type)
Index("idx_permission_status", Permission.status)


class Menu(Base, BaseMixin):
    __tablename__ = "menus"
    menu_id = Column(Integer, primary_key=True, autoincrement=True, comment="菜单ID")
    menu_name = Column(String(50), nullable=False, comment="菜单名称")
    menu_type = Column(
        Enum(MenuTypeEnum),
        default=MenuTypeEnum.CATALOG,
        nullable=False,
        comment="菜单类型:目录或菜单",
    )
    icon = Column(String(100), comment="菜单图标")
    access_path = Column(String(200), nullable=False, comment="访问路径")

    parent_menu_id = Column(Integer, ForeignKey("menus.menu_id"), comment="父级菜单ID")
    menu_level = Column(Integer, default=1, comment="菜单层级")
    order = Column(Integer, default=0, comment="排序")
    is_hidden = Column(Boolean, default=False, comment="是否隐藏")
    is_enabled = Column(Boolean, default=True, comment="是否启用")
    redirect_path = Column(String(255), comment="重定向路径")

    parent_menu = relationship(
        "Menu", remote_side=[menu_id], back_populates="children_menus"
    )
    children_menu = relationship(
        "Menu", back_populates="parent_menus", cascade="all, delete-orphan"
    )


Index("idx_menu_name", Menu.menu_name)
Index("idx_menu_type", Menu.menu_type)
Index("idx_menu_access_path", Menu.access_path)
Index("idx_menu_is_hidden", Menu.is_hidden)
Index("idx_menu_is_enabled", Menu.is_enabled)


class API(Base, BaseMixin):
    __tablename__ = "apis"
    api_id = Column(Integer, primary_key=True, autoincrement=True, comment="API ID")
    api_path = Column(String(200), nullable=False, comment="接口路径")
    request_method = Column(Enum(RequestMethodEnum), nullable=False, comment="请求方法")
    api_description = Column(String(255), comment="接口描述")
    api_tags = Column(String(255), comment="接口标签")


Index("idx_api_path", API.api_path)
Index("idx_api_request_method", API.request_method)


class UserRole(Base, BaseMixin):
    __tablename__ = "user_roles"
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        comment="用户ID",
    )
    role_id = Column(
        Integer,
        ForeignKey("roles.role_id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        comment="角色ID",
    )
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


Index("idx_user_id", UserRole.user_id)
Index("idx_role_id", UserRole.role_id)


class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id = Column(
        Integer, ForeignKey("roles.role_id"), primary_key=True, comment="角色ID"
    )
    permission_id = Column(
        Integer,
        ForeignKey("permissions.permission_id"),
        primary_key=True,
        comment="权限ID",
    )
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


Index("idx_role1_id", RolePermission.role_id)
Index("idx_permission_id", RolePermission.permission_id)


class Log(Base, BaseMixin):
    __tablename__ = "logs"
    log_id = Column(Integer, primary_key=True, autoincrement=True, comment="日志ID")
    operation_type = Column(Enum(OperationTypeEnum), nullable=False, comment="操作类型")
    object_type = Column(Enum(ObjectTypeEnum), nullable=False, comment="对象类型")
    object_id = Column(Integer, comment="对象ID")
    old_value = Column(String(255), comment="旧值")
    new_value = Column(String(255), comment="新值")


Index("idx_update_type", Log.operation_type)
Index("idx_object_id", Log.object_id)

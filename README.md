<!--
 * @Author: 王猛
 * @Date: 2024-05-10 19:10:52
 * @LastEditors: 王猛
 * @LastEditTime: 2024-05-10 22:43:18
 * @FilePath: /fastapi-project/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved. 
-->

# FastAPI 最佳实践

## 1. 项目结构。 一致且可预测

```
fastapi-project
├── alembic/
├── src # 应用程序的最高级别，包含通用模型、配置和常量等
│   ├── auth
│   │   ├── router.py   # 每个模块的核心 所有路由接口的入口
│   │   ├── schemas.py  # pydantic 模型
│   │   ├── models.py  # 数据库模型
│   │   ├── dependencies.py # 路由依赖(Depends)
│   │   ├── config.py  # 本地配置
│   │   ├── constants.py  # 特有的常量和错误码定义
│   │   ├── exceptions.py #  模块特有的异常
│   │   ├── service.py  # 特有的业务逻辑
│   │   └── utils.py  # 非业务逻辑功能，响应规范化、数据丰富等
│   ├── aws
│   │   ├── client.py  # 外部服务通信的客户端模型
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py  # 全局配置
│   ├── models.py  # 全局模型
│   ├── exceptions.py  # 全局异常
│   ├── pagination.py  # 全局模块 例如. pagination 分页
│   ├── database.py  # 数据库连接相关的东西
│   └── main.py  # 启动 FastAPI 应用程序
├── tests/
│   ├── auth
│   ├── aws
│   └── posts
├── templates/
│   └── index.html
├── requirements
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini

```

## 2. supervisor 配置

### 安装 Supervisor( Windows 不支持 )

```
pip install supervisor
```

### 自定义服务配置文件

- 生成配置文件到指定路径

```
echo_supervisord_conf > /etc/supervisord.conf
```

- 修改配置文件

```
[include]
files = /etc/supervisor/conf.d/*.ini
```

- 创建配置目录

```
mkdir /etc/supervisor/conf.d/
```

- 切换到项目目录 (/opt/fastapi-project/)

  - 创建配置文件

  ```
  vim /opt/fastapi-project/supervisor-fastapi-project.ini
  ```

  - 配置项目的进程启动参数

  ```
  ;/opt/fastapi-project/supervisor-fastapi-project.ini
  [group:autojmp]
  programs=autojmp-fastapi-project,autojmp-celery

  [program:autojmp-fastapi-project]
  command=/opt/fastapi-project/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
  directory=/opt/fastapi-project
  user=root
  autostart=true
  autorestart=unexpected
  stderr_logfile=/opt/fastapi-project/logs/fastapi-project.err.log
  stdout_logfile=/opt/fastapi-project/logs/fastapi-project.out.log

  [program:autojmp-celery]
  command=/opt/fastapi-project/venv/bin/celery -A src.tasks worker -l info
  directory=/opt/fastapi-project
  user=root
  autostart=true
  autorestart=unexpected
  stderr_logfile=/opt/fastapi-project/logs/autojmp-celery.err.log
  stdout_logfile=/opt/fastapi-project/logs/autojmp-celery.out.log

  ```

  - 配置文件链接到服务配置文件中 [include] 参数设置的目录下

  ```
  ln -s /opt/fastapi-project/supervisor-fastapi-project.ini /etc/supervisor/conf.d/fastapi-project.conf
  ```

  - 重启服务

  ```
  supervisorctl reload
  ```
- 启动服务

```
supervisord -c /etc/supervisor/conf.d/fastapi-project.conf
```

- 使用 restart, start, stop
进行进程组操作时需要加上 : 号
```
start autojmp: 启动
stop autojmp: 停止
restart autojmp: 重启
```

- 启动日志

```
tail -f /opt/fastapi-project/logs/fastapi-project.out.log
```


### 可视化操作模式

修改 服务配置文件 (/etc/supervisord.conf) 并启用以下配置

```
[inet_http_server]       
port=0.0.0.0:9001        
username=user            
password=123
```

访问 http://127.0.0.1:9001/ 输入认证密码

## 3. 项目依赖

### 安装依赖

```
pip install -r requirements/base.txt
```

### 安装依赖

```
pip install -r requirements/dev.txt
```

### 安装依赖

```
pip install -r requirements/prod.txt
```

## 3. 项目配置

### 配置文件

- 创建配置文件

```
touch .env
```

- 配置文件

```
  
`
```

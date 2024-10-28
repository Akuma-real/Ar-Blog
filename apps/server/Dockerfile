FROM python:3.9-slim as builder

WORKDIR /app

# 安装 poetry
RUN pip install poetry

# 复制项目文件
COPY pyproject.toml poetry.lock* ./
COPY app ./app

# 导出依赖
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 最终镜像
FROM python:3.9-slim

WORKDIR /app

# 复制依赖文件和应用代码
COPY --from=builder /app/requirements.txt .
COPY --from=builder /app/app ./app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

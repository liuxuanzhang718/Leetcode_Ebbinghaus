FROM python:3.11-slim

# 清除任何代理设置
ENV HTTP_PROXY=""
ENV HTTPS_PROXY=""
ENV http_proxy=""
ENV https_proxy=""

WORKDIR /app

# 使用阿里云镜像源
RUN echo \
    deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib \
    deb https://mirrors.aliyun.com/debian-security/ bullseye-security main \
    deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib \
    deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib \
    > /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
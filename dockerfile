# 使用官方的 Python 基础镜像，包含 Python 3.10+
FROM python:3.10


# 安装 poppler
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 复制到容器中
COPY requirements.txt .

# 安装 Python 依赖
# RUN python -m pip install --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录下的所有文件复制到容器的 /app 目录下
COPY . .

# 暴露端口 8888
EXPOSE 8888

# 启动应用
# CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "--timeout 120", "app:app"]

# 使用基础镜像
FROM python:3

# 设置工作目录
WORKDIR /app

# 复制funasr-server可执行文件和启动脚本到镜像中
COPY funasr-server.py /app
COPY funasr_wss_client.py  /app
COPY requirements_client.txt /app
RUN  pip3 install -r /app/requirements_client.txt

# 启动funasr-server服务
CMD ["python3", "/app/funasr-server.py"]


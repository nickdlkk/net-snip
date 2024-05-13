FROM python:3.11.0
LABEL authors="Nick"

# 设置工作目录为/app
WORKDIR /app
# 将当前目录下的所有文件打包进入镜像
ADD . /app

# 安装requirements.txt中指定的Python包
RUN pip install -r /app/requirements.txt

EXPOSE 5000
# 设置容器启动时执行的命令
CMD ["python", "index.py"]

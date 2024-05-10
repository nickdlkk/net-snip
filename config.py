import os
from dotenv_vault import load_dotenv
import sys

try:
    load_dotenv()
except FileNotFoundError:
    print(".env file not found! Using default or fallback settings.")

# 获取第一个参数
if len(sys.argv) > 1:
    env_state = sys.argv[1]
    print(f".env.{env_state}")
    # 加载特定环境的环境变量
    # 第一个参数如果获取不到对应文件需要写成绝对路径 借助Path(__file__)获取路径
    # 第二个参数override=True表示当已存在同名环境变量时 用特定的环境变量值进行覆盖
    load_dotenv(f".env.{env_state}", override=True)


class Config:
    sqlite_db_name = 'net_snip.db'
    default_word_length = 5
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_database = os.getenv("POSTGRES_DATABASE")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")

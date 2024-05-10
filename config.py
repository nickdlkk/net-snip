import os
from dotenv_vault import load_dotenv
import sys

load_dotenv(verbose=True)

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
    db_host = os.getenv("host")
    db_port = os.getenv("port")
    db_database = os.getenv("database")
    db_user = os.getenv("user")
    db_password = os.getenv("password")

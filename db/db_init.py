from config import Config
import psycopg2


def init():
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:

        # 创建游标对象
        cur = conn.cursor()
        # 创建表的 SQL 语句
        # 读取 SQL 文件内容
        with open('db/init.sql', 'r') as file:
            sql_script = file.read()
        # 执行 SQL 语句
        try:
            cur.execute(sql_script)
            conn.commit()
            print("Table created successfully")
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()

import sqlite3
import psycopg2
import random
import string
from config import Config
import datetime
import hashlib


def random_string(length):
    """
    获取随机生成的
    """
    with sqlite3.connect(Config.sqlite_db_name) as conn:
        random_string_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        select_random = "SELECT 'key' FROM enwords where 'key' like '{word}';"
        cursor = conn.cursor()
        cursor.execute(select_random.format(word=random_string_str))
        select_random = cursor.fetchone()
        if select_random == None:
            return random_string_str
        else:
            random_string_str = random_string()
            return random_string_str


def get_new_key(word_length):
    with sqlite3.connect(Config.sqlite_db_name) as conn:
        cursor = conn.cursor()
        select_word = 'SELECT word FROM enwords where LENGTH(word) < {word_length} ORDER BY RANDOM()  limit 1 ;'
        select_word_sql = select_word.format(word_length=word_length)
        cursor.execute(select_word_sql)
        # 取到值
        word = cursor.fetchone()
        print(word)
        random_string_str = ""
        if word is None:
            # 生成随机字符串，包含小写字母和数字
            random_string_str = random_string(word_length)
        else:
            random_string_str = word[0]
        # 关闭游标
        cursor.close()
        return random_string_str


def check_key_exist(key_name):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        select = 'SELECT id FROM snip_key where key = %s;'
        cursor.execute(select, (key_name,))
        result = cursor.fetchone()
        cursor.close()
        return result


def save_key(key, password):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        insert_sql = "INSERT INTO snip_key (key, create_time, update_time, password) VALUES (%s,%s,%s,%s);"
        cursor.execute(insert_sql, (key, datetime.datetime.now(), datetime.datetime.now(), password))
        conn.commit()


def get_by_key(key):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        select = 'SELECT k.id,k.key,k.create_time,k.update_time,v.value,v.update_time as content_update_time,k.password  FROM snip_key k left join snip_value v on k.id = v.key_id where key like %s order by v.update_time desc;'
        cursor.execute(select, (key,))
        results = cursor.fetchall()  # 获取所有查询结果
        if results is None:
            results = []
        # 获取列名
        columns = [col[0] for col in cursor.description]
        # 将每行数据转换为字典
        result_dicts = [dict(zip(columns, row)) for row in results]
        return result_dicts


def check_key_pwd(key, password):
    if password is None:
        password = ''
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        select = 'SELECT key,password FROM snip_key where key like %s;'
        cursor.execute(select, (key,))
        # 取到值
        info = cursor.fetchone()
        print(info)
        if info is None:
            return True
        print(info[0] == key , info[1] == password)
        if info[0] == key and info[1] == password:
            print("密码正确")
            return True
        else:
            return False


def update_password(key_id, password):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        update = "UPDATE snip_key SET password = %s WHERE id = %s;"
        cursor.execute(update, (password, key_id))
        conn.commit()


def save_content(key_id, content, time):
    insert_sql = "INSERT INTO snip_value (key_id, value, update_time) VALUES (%s, %s, %s);"
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_sql, (key_id, content, time))
        conn.commit()


def insert_file(key_id, file, file_md5, file_name, file_size):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        insert_sql = "INSERT INTO snip_files (key_id, file, file_md5, create_time,file_name,file_size) VALUES(%s, %s, %s, %s, %s, %s);"
        cursor = conn.cursor()
        cursor.execute(insert_sql,
                       (key_id, psycopg2.Binary(file), file_md5, datetime.datetime.now(), file_name, file_size))
        conn.commit()


def list_file(key_id):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        select = 'SELECT id,key_id,create_time,file_name,file_size,file_md5 from snip_files where key_id = %s order by create_time desc;'
        cursor.execute(select, (key_id,))
        results = cursor.fetchall()  # 获取所有查询结果
        cursor.close()
        if results is None:
            results = []
        # 获取列名
        columns = [col[0] for col in cursor.description]
        # 将每行数据转换为字典
        result_dicts = [dict(zip(columns, row)) for row in results]
        return result_dicts


def get_key_file_total_size(key_id):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cursor = conn.cursor()
        select = 'select SUM(file_size) from snip_files where key_id = %s;'
        cursor.execute(select, (key_id,))
        results = cursor.fetchone()  # 获取所有查询结果
        cursor.close()
        if results is not None:
            if results[0] is None:
                return 0
            return results[0]
        else:
            return 0


def get_file(id, key_id):
    with psycopg2.connect(host=Config.db_host,
                          port=Config.db_port,
                          database=Config.db_database,
                          user=Config.db_user,
                          password=Config.db_password) as conn:
        cur = conn.cursor()
        cur.execute("SELECT file, file_md5,file_name FROM snip_files WHERE id = %s and key_id = %s", (id, key_id))
        file_data, stored_md5_hash, file_name = cur.fetchone()
        cur.close()
        return file_data, file_name


if __name__ == '__main__':
    file = open("index.py", 'rb').read()
    md5 = hashlib.md5(file).hexdigest()
    insert_file(1, file, md5, "index.py")

    file_list = list_file(1)
    print(file_list)
    for file in file_list:
        file_data = get_file(file['id'], file['key_id'])
        file_data_bytes = bytes(file_data)
        # 尝试以 UTF-8 编码解码字节串
        try:
            file_data_str = file_data_bytes.decode('utf-8')
        except UnicodeDecodeError:
            file_data_str = "无法以 UTF-8 编码解码此二进制数据"

        print(file_data_str)

import sqlite3
import random
import string
from config import Config
import time


def random_string(length):
    with sqlite3.connect(Config.db_name) as conn:
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
    with sqlite3.connect(Config.db_name) as conn:
        cursor = conn.cursor()
        select_word = 'SELECT word FROM enwords where LENGTH(word) < {word_length} and word not in (select key from snip_key)  ORDER BY RANDOM()  limit 1 ;'
        select_word_sql = select_word.format(word_length=word_length)
        cursor.execute(select_word_sql)
        # 取到值
        word = cursor.fetchone()
        print(word)
        random_string_str = ""
        if word == None:
            # 生成一个长度为5的随机字符串，包含小写字母和数字
            random_string_str = random_string(word_length)
        else:
            random_string_str = word[0]
        # 关闭游标
        cursor.close()
        return random_string_str


def save_key(key, password):
    with sqlite3.connect(Config.db_name) as conn:
        cursor = conn.cursor()
        insert_sql = "INSERT INTO snip_key (key, create_time, update_time,password)VALUES (?, ? ,?,?);"
        cursor.execute(insert_sql, (key, int(time.time()), int(time.time()), password))
        conn.commit()


def get_by_key(key):
    with sqlite3.connect(Config.db_name) as conn:
        cursor = conn.cursor()
        select = 'SELECT k.id,k.key,k.create_time,k.update_time,v.value,v.update_time as content_update_time,k.password   FROM snip_key k left join snip_value v on k.id = v.key_id where key like ? order by v.update_time desc;'
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
    with sqlite3.connect(Config.db_name) as conn:
        cursor = conn.cursor()
        select = 'SELECT key,password FROM snip_key where key like ?;'
        cursor.execute(select, (key,))
        # 取到值
        info = cursor.fetchone()
        print(info)
        if info is None:
            return False
        if info[0] == key and info[1] == password:
            return True
        else:
            return False


def update_password(key_id, password):
    with sqlite3.connect(Config.db_name) as conn:
        cursor = conn.cursor()
        update = "UPDATE snip_key SET password = ? WHERE id = ?;"
        cursor.execute(update, (password, key_id))
        conn.commit()


def save_content(key_id, content, time):
    insert_sql = "INSERT INTO snip_value (key_id, value, update_time) VALUES (?, ?, ?);"
    with sqlite3.connect(Config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_sql, (key_id, content, time))
        conn.commit()

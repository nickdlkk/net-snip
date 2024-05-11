import hashlib

from pywebio.utils import parse_file_size

import model
from config import Config


def upload_file(key_id, files):
    total_size_config = parse_file_size(Config.file_limit_total_size)
    total_size = model.get_key_file_total_size(key_id)
    current_size = sum(file['size'] for file in files)
    print(f"{total_size_config} {total_size}")
    print(f" {current_size + total_size}")
    if current_size + total_size > total_size_config:
        return "文件大小超出限制"
    for file in files:
        file_name = file['filename']
        file_size = file['size']
        file_content = file['content']
        md5 = hashlib.md5(file_content).hexdigest()
        model.insert_file(key_id, file_content, md5, file_name, file_size)
    return "上传成功"




if "__main__" == __name__:
    upload_file(1, None, None)

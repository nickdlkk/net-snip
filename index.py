import hashlib
from urllib.parse import quote

import pywebio
from flask import request

import model
from network_snip import main

app = pywebio.platform.flask.wsgi_app(main)


@app.route('/download', methods=['GET'])
def download_file():
    # 获取请求参数
    file_md5 = request.args.get('m')
    key_id = request.args.get('kid')
    id = request.args.get('fid')

    file_data, file_name = model.get_file(id, key_id)
    # 校验MD5哈希值
    calculated_md5_hash = hashlib.md5(file_data).hexdigest()
    if calculated_md5_hash == file_md5:
        print("MD5哈希值校验成功。")
    else:
        print("MD5哈希值校验失败。")
        return "文件校验失败，可能存在数据损坏。", 400
    # 创建一个响应对象，直接返回文件数据
    response = app.response_class(
        response=file_data,
        status=200,
        mimetype='application/octet-stream',
        headers={
            "Content-Disposition": f"attachment;filename={quote(file_name)}",
            "Content-Type": "application/octet-stream",
        }
    )

    return response


if __name__ == '__main__':
    print("app start")
    app.run(debug=True)

import datetime
import uuid

import pywebio_battery
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import local, defer_call
from pywebio.session import set_env, download, run_js

import model
import service
import store
from config import Config
from db import db_init
from utils.Debounce import Debounce
from view import View

debouncer = Debounce(5)  # 创建一个防抖对象，设置间隔时间为5秒
db_init.init()


def main():
    set_env(title='网络剪贴板', output_animation=False)
    local.uid = uuid.uuid4()
    key = pywebio_battery.get_query("key")
    if key is None:
        put_button("generate new key", onclick=generate_new_key)
        key = input("输入key")
        check_key_exist(key)
        js = """
                let url = new URL(window.location.href);
                url.searchParams.set('key', key);
                window.location.href = url.toString();
                """
        run_js(js, key=key)
    else:
        pwd = pywebio_battery.get_query("password")
        if check_key_exist(key):
            check_password(key, pwd)
        snip(key, pwd)


def check_key_exist(key):
    """
    检查key是否存在 不存在则创建key
    不存在返回False 存在返回True
    """
    with put_loading():
        put_text("Check key ...")
        result = model.check_key_exist(key)
    if result is None:
        with put_loading():
            put_text("Save new key ...")
            model.save_key(key, "")
        return False
    else:
        return True


def generate_new_key():
    # 生成新key后跳转
    js = """
            let url = new URL(window.location.href);
            url.searchParams.set('key', key);
            window.location.href = url.toString();
            """
    with put_loading():
        put_text("Generate new key ...")
        key = model.get_new_key(Config.default_word_length)
        model.save_key(key, "")
    run_js(js, key=key)


def rander_update_password():
    with use_scope(View.password_scop, clear=True):
        put_text("update password:")
        put_input(View.update_password, type=PASSWORD)
        put_button("update password", onclick=change_password)


def check_password(key, password):
    """
    循环检查密码是否正确
    正确返回True 错误返回False
    """
    local.key = key
    kv = store.get_local()
    print(password)
    if kv is not None and kv.get(key) is not None and (password is not None or password != ""):
        password = kv.get(key)
        print("cache password:" + password)
    with put_loading():
        put_text("Check password...")
        key_pwd = model.check_key_pwd(key, password)
    pwd = ''
    if not key_pwd:
        print("check password error")
        with use_scope(View.password_scop):
            kv[key] = ''
            pwd = input("Input password", type=PASSWORD)
            print("pwd", pwd)
        check_password(key, pwd)
    else:
        print("check password success")


def snip(key, password):
    local.key = key
    kv = store.get_local()
    with put_loading():
        put_text("Loading data ...")
        content_value = model.get_by_key(key)
    kv[key] = password
    store.save_local(kv)
    local.key_id = content_value[0]['id']

    put_text("key:", key)

    rander_update_password()
    put_row([
        put_text("create time:", content_value[0]["create_time"].strftime("%Y-%m-%d %H:%M:%S")),
        put_text("update time:", content_value[0]["update_time"].strftime("%Y-%m-%d %H:%M:%S"))
    ])
    put_markdown("""# Markdown Live Preview
    The online markdown editor with live preview. The source code of this application is [here](https://github.com/wang0618/PyWebIO/blob/dev/demos/markdown_previewer.py).
    ## Write your Content With Markdown
    """)
    render_file_scop()

    with use_scope(View.update_time_scop):
        time_ = content_value[0]["content_update_time"]
        if time_ is not None:
            put_text("content update time:", time_)
    # 添加监听更新线程
    service.add_watch_thread(local.key, local.uid)
    with use_scope('md_text_scope', clear=True):
        put_textarea('md_text', rows=18, code={'mode': 'markdown'}, value=content_value[0]["value"])
    put_row([
        put_buttons(['Download content'], lambda _: download('saved.md', pin.md_text.encode('utf8')), small=True),
        put_buttons(['Save'], onclick=save_content, small=True)
    ])
    put_markdown('## Preview')

    with use_scope('md', clear=True):
        value_ = content_value[0]["value"]
        if value_ is not None:
            put_markdown(value_, sanitize=False)

    while True:
        change_detail = pin_wait_change('md_text')
        with use_scope('md', clear=True):
            put_markdown(change_detail['value'], sanitize=False)
            pin_wait_change_save(change_detail)


def render_file_scop():
    with use_scope('files', clear=True):
        put_file_upload("SelectFile", label='Upload File', accept="*/*", multiple=True,
                        max_size=Config.file_limit_size,
                        max_total_size=Config.file_limit_total_size)
        put_button('Upload', onclick=file_upload_onclick)
        with put_loading():
            put_text("Loading Data...")
            files = model.list_file(local.key_id)
        for file in files:
            put_link("{} (size :{} create time: {})".format(file['file_name'], file['file_size'],
                                                            file['create_time'].strftime("%Y-%m-%d %H:%M:%S")),
                     url="/download?m={}&fid={}&kid={}".format(file['file_md5'], file['id'], local.key_id),
                     new_window=True)
        # put_button('Download', onclick=lambda _: pin.file.download_file(model.download_file))


def file_upload_onclick():
    print(f'file_upload_onclick')
    files = pin['SelectFile']
    if files is None or len(files) == 0:
        toast("请选择文件.")
        return
    with put_loading(shape='grow'):
        put_text("Uploading File...")
        return_str = service.upload_file(local.key_id, files)
    toast(return_str)
    if return_str == "上传成功":
        render_file_scop()


def change_password():
    """
    更新密码
    """
    key_id = local.key_id
    password_ = pin[View.update_password]
    model.update_password(key_id, password_)
    kv = store.get_local()
    kv[local.key] = password_
    store.save_local(kv)
    rander_update_password()
    toast("update success!", color='success')


def save_content(val):
    # 主动保存后,取消自动保存
    if val == "Save":
        debouncer.cancel()
    with use_scope(View.update_time_scop, clear=True):
        with put_loading(shape='grow'):
            put_text("Saving Content...")
            print(f"save_content {val}")
            key_id = local.key_id
            print("save key_id:{}".format(key_id))
            print(pin['md_text'])
            time_now = datetime.datetime.now()
            model.save_content(key_id, pin['md_text'], time_now)
            service.push_watch_event(local.key, local.uid, pin['md_text'])
    with use_scope(View.update_time_scop, clear=True):
        put_text("content update time:", time_now.strftime("%Y-%m-%d %H:%M:%S"))
    toast("save success!", color='success')


@debouncer.debounce
def pin_wait_change_save(input_var):
    print(f"pin_wait_change_save received: {input_var}")
    save_content(input_var)


# @defer_call
# def cleanup():
#     service.del_watch_thread(local.key, local.uid)

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)

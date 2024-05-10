"""
网络剪辑版
1. 复用Markdown Previewer Demo
2. 数据保存到Sqlite
3.
"""
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env, download, info, run_js, register_thread
import model
import store
import pywebio_battery

from net_snip.config import Config
from pywebio.session import local

from net_snip.utils.Debounce import Debounce
import datetime

from net_snip.view import View

debouncer = Debounce(5)  # 创建一个防抖对象，设置间隔时间为5秒


def main():
    set_env(output_animation=False)
    key = pywebio_battery.get_query("key")
    pwd = pywebio_battery.get_query("password")
    if key is None:
        key = model.get_new_key(Config.default_word_length)
        # 生成新key后跳转
        js = """
        let url = new URL(window.location.href);
        url.searchParams.set('key', key);
        window.location.href = url.toString();
        """
        model.save_key(key, "")
        run_js(js, key=key)
    else:
        snip(key, pwd)

def rander_update_password():
    with use_scope(View.password_scop, clear=True):
        put_text("update password:")
        put_input(View.update_password, type=PASSWORD)
        put_button("update password", onclick=change_password)
def snip(key, password):
    local.key = key
    # model.save_key(key)
    kv = store.get_local()
    if kv is not None and kv.get(key) is not None and password != "":
        password = kv.get(key)
        print("cache password:" + password)

    if not model.check_key_pwd(key, password):
        print("check password error")
        with use_scope(View.password_scop):
            put_text("enter password:")
            pwd = input("Input password", type=PASSWORD)
        snip(key, pwd)
    else:
        content_value = model.get_by_key(key)
        kv[key] = password
        store.save_local(kv)
        local.key_id = content_value[0]['id']

        put_text("key:", key)

        rander_update_password()

        put_text("create time:", datetime.datetime.fromtimestamp(content_value[0]["create_time"]))
        put_text("update time:", datetime.datetime.fromtimestamp(content_value[0]["update_time"]))
        put_markdown("""# Markdown Live Preview
        The online markdown editor with live preview. The source code of this application is [here](https://github.com/wang0618/PyWebIO/blob/dev/demos/markdown_previewer.py).
        ## Write your Content With Markdown
        """)
        with use_scope(View.update_time_scop):
            put_text("content update time:", datetime.datetime.fromtimestamp(content_value[0]["content_update_time"]))
        put_textarea('md_text', rows=18, code={'mode': 'markdown'}, value=content_value[0]["value"])

        put_buttons(['Download content'], lambda _: download('saved.md', pin.md_text.encode('utf8')), small=True)
        put_buttons(['Save'], onclick=save_content, small=True)

        put_markdown('## Preview')

        with use_scope('md', clear=True):
            put_markdown(content_value[0]["value"], sanitize=False)

        while True:
            change_detail = pin_wait_change('md_text')
            with use_scope('md', clear=True):
                put_markdown(change_detail['value'], sanitize=False)
                pin_wait__change_save(change_detail)


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
    print(f"save_content {val}")
    key_id = local.key_id
    print("save key_id:{}".format(key_id))
    print(pin['md_text'])
    time_now = int(datetime.datetime.now().timestamp())
    model.save_content(key_id, pin['md_text'], time_now)
    with use_scope(View.update_time_scop, clear=True):
        put_text("content update time:", datetime.datetime.fromtimestamp(time_now))
    toast("save success!", color='success')


@debouncer.debounce
def pin_wait_change_save(input_var):
    print(f"pin_wait_change_save received: {input_var}")
    save_content(input_var)


if __name__ == '__main__':
    start_server(main, port=8080, debug=True)

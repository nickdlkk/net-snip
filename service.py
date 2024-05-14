import hashlib
import threading
from io import BytesIO

import qrcode
from pywebio.output import use_scope, put_text, put_row, put_button, put_markdown
from pywebio.pin import put_textarea
from pywebio.session import register_thread
from pywebio.utils import parse_file_size

import model
from config import Config
from view import View

thread_dict = {}


class WatcherThread(threading.Thread):
    def __init__(self, key, uid, event):
        super().__init__()
        self.key = key
        self.uid = uid
        self.event = event
        self.stop = False

    def run(self):
        while not self.stop:
            print('%s waiting for event' % threading.current_thread().name)
            self.event.wait()  # 等待事件发生
            if self.stop:
                break
            print('%s event received' % threading.current_thread().name)
            with use_scope(View.update_time_scop):
                put_row([
                    put_text("当前剪贴板有更新!"),
                    put_button("点击更新", onclick=self.update_content)
                ])
            self.event.clear()

    def update_content(self):
        data = self.event.data
        with use_scope('md_text_scope', clear=True):
            put_textarea('md_text', rows=18, code={'mode': 'markdown'}, value=data)
        with use_scope('md', clear=True):
            put_markdown(data, sanitize=False)
        with use_scope(View.update_time_scop, clear=True):
            put_text("剪贴板已更新")

    def stop_thread(self):
        self.stop = True
        self.event.set()


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


def add_watch_thread(key, uid):
    """
    将线程添加到线程池中
    :param key: 线程的key
    :param uid: 用户id
    :param thread: 线程对象
    """

    if key not in thread_dict:
        thread_dict[key] = {}
    event = threading.Event()
    thread = WatcherThread(key, uid, event)
    register_thread(thread)
    thread.start()
    if len(thread_dict[key]) == 0:
        thread_dict[key] = []
    thread_dict[key].append({"key": key, "uid": uid, "thread": thread, "event": event})
    return thread


def del_watch_thread(key, uid):
    for e in thread_dict[key]:
        if e['key'] == key and e['uid'] == uid:
            e["thread"].stop_thread()
            thread_dict[key].remove(e)
            return


def push_watch_event(key, uid, data):
    for t in thread_dict[key]:
        if t['uid'] == uid:
            continue
        t['event'].data = data
        t['event'].set()


def get_qrcode(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # 将图片保存到字节流中
    byte_io = BytesIO()
    img.save(byte_io)
    byte_io.seek(0)

    # 获取字节类型数据
    byte_data = byte_io.read()

    return byte_data


if __name__ == '__main__':
    # upload_file(1, None, None)
    img = get_qrcode("https://github.com/")
    print(img)
    # img.save('qrcode.png')

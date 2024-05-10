import pywebio

from network_snip import main

if __name__ == '__main__':
    pywebio.platform.flask.start_server(main, port=80)

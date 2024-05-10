import pywebio

from network_snip import main

pywebio.platform.flask.start_server(main)

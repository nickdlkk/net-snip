import pywebio

from network_snip import main

app =  pywebio.platform.flask.start_server(main)

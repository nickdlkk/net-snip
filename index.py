# import pywebio
from pywebio.platform.fastapi import asgi_app

from network_snip import main

app = asgi_app(main)
# handler =  pywebio.platform.flask.wsgi_app(main)

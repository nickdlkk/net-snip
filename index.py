import pywebio

from network_snip import main

handler =  pywebio.platform.flask.wsgi_app(main)

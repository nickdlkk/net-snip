import pywebio

from network_snip import main

pywebio.platform.flask.wsgi_app(main)

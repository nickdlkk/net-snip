import pywebio

from network_snip import main

app = pywebio.platform.flask.wsgi_app(main)
app.run()

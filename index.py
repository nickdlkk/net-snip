import pywebio

from network_snip import main

app = pywebio.platform.flask.wsgi_app(main)

if __name__ == '__main__':
    print("app start")
    app.run(debug=True)

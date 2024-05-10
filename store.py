import json

import pywebio_battery

'''
The data is specific to the origin (protocol+domain+port) of the app. Different origins use different web browser local storage.
'''


def save_local(kv):
    pywebio_battery.set_localstorage('config', json.dumps(kv))


def get_local():
    localstorage = pywebio_battery.get_localstorage('config')
    return {} if localstorage is None else json.loads(localstorage)

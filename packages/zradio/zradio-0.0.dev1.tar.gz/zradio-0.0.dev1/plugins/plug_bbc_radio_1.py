import json
import requests
import time
from threading import Thread

from notify import Notification

from plugins import FrozenJson

URL = "http://np.radioplayer.co.uk/qp/v3/onair?rpIds=340&nameSize=200&artistNameSize=200&descriptionSize=200"


def get_data(url):
    resp = requests.get(url)
    data = json.loads(resp.text[9:-1])
    return data


def run():
    data = FrozenJson(get_data(URL))
    objs = []
    try:
        if data.results._340:
            for obj in data.results._340:
                try:
                    objs.append(obj)
                except Exception as exc:
                    print(exc)
            service = objs[-1].serviceName
            artist = objs[-1].artistName
            song = objs[-1].name
            return service, artist, song
    except Exception as exc:
        print(exc)
        return "(*_*)", "(*_*)", "(*_*)"

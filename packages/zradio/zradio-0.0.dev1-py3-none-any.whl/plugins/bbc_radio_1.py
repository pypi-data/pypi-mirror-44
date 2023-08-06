import json
import requests
import threading
import time

from radio.log import logger

from notify import Notification

URL = "http://np.radioplayer.co.uk/qp/v3/onair?rpIds=340&nameSize=200&artistNameSize=200&descriptionSize=200"


from collections import abc
from keyword import iskeyword


class FrozenJson:
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += "_"
            elif str(key).isnumeric():
                key = "_" + key
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson.build(self.__data[name])

    def __repr__(self):
        return "FrozenJson(%r)" % (self.__data)

    @classmethod
    def build(cls, obj):

        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


def get_data(url):
    resp = requests.get(url)
    data = json.loads(resp.text[9:-1])
    return data


def music_name(url):

    while True:
        data = get_data(url)
        data = FrozenJson(data)
        objs = []
        if data.results._340:
            for obj in data.results._340:
                try:
                    objs.append(obj)
                except Exception as error:
                    print(error)
            logger.info(objs[-1])
            artist_name = objs[-1].artistName
            music_name = objs[-1].name
            msg = f"Artist: {artist_name}\nSong: {music_name}"
            Notification(objs[-1].serviceName, msg)
        time.sleep(60 * 2)


class Plugin:
    def __init__(self, **context):
        pass

    def run(self):
        threading.Thread(target=music_name, args=(URL,), daemon=True).start()

import importlib
import time

from queue import Queue
from threading import Event
from threading import Thread

import vlc

from notify import Notification
from pyradios import RadioBrowser

from radio.log import logger
from radio.models import Station

play_now = Queue(1)


class RunPlugin(Thread):
    def __init__(self, func):
        super().__init__()
        self.daemon = True
        self.func = func
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        msg = "Service: {} \nArtist: {}\nSong: {}"
        while not self.stopped():
            resp = self.func()
            logger.info(msg.format(*resp))
            Notification(resp[0], msg.format(*resp))
            time.sleep(60)


class Player:

    instance = vlc.Instance("--verbose -1")
    player = instance.media_player_new()
    plugins = []
    plug = None
    station = None

    def run_plugin(self):
        p = RunPlugin(self.plug.run)
        p.start()
        self.plugins.append(p)

    def kill_plugin(self):
        try:
            self.plugins[0].stop()
            self.plugins.pop()
        except IndexError as exc:
            logger.debug(exc)


class Play(Player):
    def __init__(self, station):
        super().__init__()
        self.station = station

    def __call__(self):

        self.plug = self.station.load_plugin()

        if self.plug:
            self.run_plugin()
        else:
            self.kill_plugin()

        media = self.instance.media_new(self.station.url)
        self.player.set_media(media)
        self.player.play()


class Stop(Player):
    def __init__(self):
        super().__init__()

    def __call__(self):
        self.kill_plugin()
        self.player.stop()


class Radio(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.start()  # inicia a thread

    def run(self):

        while True:
            logger.info(play_now)
            obj = play_now.get()  # block until an item is available
            if isinstance(obj, Play):  # TODO: remove this line
                obj()
            if isinstance(obj, Stop):
                obj()

            if isinstance(obj, Station):
                p = Play(obj)
                p()


radio = Radio()

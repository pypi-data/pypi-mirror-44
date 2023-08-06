from queue import Queue
from threading import Thread


import vlc


play_now = Queue(1)


class Player(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.instance = vlc.Instance("--verbose -1")
        self.player = self.instance.media_player_new()
        self.start()

    def run(self):
        obj = play_now.get()
        media = self.instance.media_new(obj.url)
        self.player.set_media(media)
        try:
            self.player.play()
            while not play_now.full():
                pass
            else:
                self.player.stop()
        except KeyboardInterrupt:
            self.player.stop()

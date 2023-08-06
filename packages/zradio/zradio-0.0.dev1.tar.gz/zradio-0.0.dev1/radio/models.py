from radio.log import logger

import importlib

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.widgets import TextArea


from pyradios import RadioBrowser


class Station:
    plug = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def printable(self):
        return f"{self.id:<6} | > {self.name[0:30]:<30} | tags: {self.tags}\n"

    def path_to_plugin(self):
        return "_".join(self.name.split(" ")).lower()

    def load_plugin(self):
        try:
            self.plug = importlib.import_module("plugins.plug_" + self.path_to_plugin())
            return self.plug
        except ImportError as exc:
            logger.debug(exc)
        return None

    def play_now(self):
        msg = "Service: {}\nArtist: {}\nSong: {}"
        return msg

    def show_info(self):
        msg = f"{self.id} | > {self.name}\n\n\n {self.url}"
        return msg

    def __repr__(self):
        return f"{self.name}"


class Radios:
    def __init__(self, data):
        self._data = [Station(**obj) for obj in data]
        self._content = "".join(line.printable() for line in self.data)

    @property
    def content(self):
        return self._content

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, other):
        self._data = [Station(**obj) for obj in other]
        self._content = "".join(line.printable() for line in self._data)

    def get_obj(self, index):
        return self.data[index]


# Initialize RadioBrowser
radio_browser = RadioBrowser()

radios = Radios(radio_browser.stations_bytag("bbc"))

# Create list_buffer
# to reset buffer -> buffer.reset(Document(text, 0))

list_buffer = Buffer(
    document=Document(radios.content, 0),
    multiline=True,
    read_only=True,
    name="list_buffer",
)


# Create command_buffer
command_buffer = Buffer(
    completer=WordCompleter(
        ["play", "info", "help", "stations", "bytag", "byid", "exit"], ignore_case=True
    ),
    complete_while_typing=True,
    name="command_buffer",
)
# Create info_area
# info_area = TextArea(focusable=True, read_only=True)
doc = Document("", 0)
info_area = Buffer(document=doc, read_only=True)

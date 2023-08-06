from queue import Queue


from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

display = Queue(1)


class DisplayBuffer:
    def __init__(self):
        self._document = Document("", 0)
        self._buffer = Buffer(document=self._document, read_only=True)

    @property
    def document(self):
        return self._document

    @document.set
    def document(self, text):
        self._document = Document(text, 0)

    @property
    def buffer(self):
        return self._buffer

    @buffer.set
    def buffer(self, doc=None):
        self._buffer.set_document(doc, bypass_readonly=True)

    def update_buffer(self):
        self._buffer.set_document(self._document, bypass_readonly=True)

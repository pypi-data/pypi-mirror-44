from radio.log import logger

from prompt_toolkit.layout import BufferControl
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout import HSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import Box


from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout import FloatContainer
from prompt_toolkit.layout import Float
from prompt_toolkit.layout import CompletionsMenu
from prompt_toolkit.layout.processors import BeforeInput


from radio.commands import handle_command


class ListView:
    def __init__(self, buffer):

        self._buffer = buffer
        self.buffer_control = BufferControl(
            buffer=self._buffer,
            focusable=True,
            key_bindings=self._get_key_bindings(),
            focus_on_click=True,
        )

        self.window = Window(
            content=self.buffer_control,
            right_margins=[ScrollbarMargin(display_arrows=True)],
        )
        self.window = HSplit(
            [Box(self.window, padding_left=2, padding_right=0)]
        )

    def handler(self, event):
        # return -> int line number
        index = self._buffer.document.cursor_position_row
        # return -> str line
        text = self._buffer.document.current_line
        return handle_command(event, index=index, text=text)

    def _get_key_bindings(self):
        " Key bindings for the List. "
        kb = KeyBindings()

        @kb.add("p")
        @kb.add("enter")
        def _(event):
            if self.handler is not None:
                self.handler(event)

        return kb

    def __pt_container__(self):
        return self.window


def command_prompt(buffer, key_bindings, **kwargs):

    before_input_text = kwargs.get("before_input_text", "➜ ")
    title = kwargs.get("title", "COMMAND SHELL")

    prompt = Frame(
        title=title,
        key_bindings=key_bindings(),
        body=FloatContainer(
            content=Window(
                BufferControl(
                    buffer=buffer,
                    input_processors=[BeforeInput(text=before_input_text)],
                )
            ),
            key_bindings=None,
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=5, scroll_offset=1),
                )
            ],
        ),
        height=3,
    )
    return prompt

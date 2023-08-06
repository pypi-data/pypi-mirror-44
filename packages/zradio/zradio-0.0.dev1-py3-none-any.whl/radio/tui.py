from radio.log import logger

from prompt_toolkit.application import Application
from prompt_toolkit.application import get_app

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.focus import focus_previous

from prompt_toolkit.layout import BufferControl
from prompt_toolkit.layout import Float
from prompt_toolkit.layout import FloatContainer
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout import VSplit
from prompt_toolkit.layout import HSplit
from prompt_toolkit.layout import CompletionsMenu
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.layout.processors import BeforeInput

from prompt_toolkit.widgets import Box
from prompt_toolkit.widgets import Label
from prompt_toolkit.widgets import Frame


from radio.models import command_buffer
from radio.models import list_buffer
from radio.models import info_area

from radio.styles import style

from radio.commands import handle_command


class TopMessage:
    def __init__(self, app):
        self.app = app
        self.window = Box(
            Label(
                text="Press `shift UP` or `shift Down` to move the focus; Press `Ctrl + Q` to quit."
            ),
            padding_left=2,
        )

    def __pt_container__(self):
        return self.window


# class Display:
#     def __init__(self, app):
#         self.app = app
#         self.window = Frame(
#             HSplit([Box(info_area, padding_top=2, padding_left=2)]), height=10
#         )
#
#     def __pt_container__(self):
#         return self.window


class Display:
    def __init__(self, buffer):
        self._buffer = buffer
        self.buffer_control = BufferControl(
            buffer=self._buffer, focusable=True, focus_on_click=True
        )
        self.window = Window(content=self.buffer_control)
        # self.window = HSplit([Box(info_area, padding_top=2, padding_left=2)]), height=10)
        self.window = Frame(body=Box(self.window, padding_left=2, padding_right=0))

    def __pt_container__(self):
        return self.window


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
        self.window = Frame(body=Box(self.window, padding_left=2, padding_right=0))

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


class CommandPrompt:
    def __init__(self, buffer, **kwargs):
        self.buffer = buffer
        self.before_input_text = kwargs.get("before_input_text", "➜ ")
        self.title = kwargs.get("title", "COMMAND SHELL")
        self._buffer = buffer
        self._buffer_control = BufferControl(
            buffer=self.buffer,
            input_processors=[BeforeInput(text=self.before_input_text)],
        )
        self.window = Frame(
            title=self.title,
            key_bindings=self.kbindings(),
            body=FloatContainer(
                content=Window(self._buffer_control),
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

    def kbindings(self):

        kb = KeyBindings()

        @kb.add("enter")
        def _(event):
            handle_command(event)
            command_buffer.text = ""

        @kb.add("c-@")
        def _(event):
            print("aqui")

        return kb

    def __pt_container__(self):
        return self.window


class AppLayout:
    def __init__(self, *args, **kwargs):
        pass


class App:
    def __init__(self, *args, **kwargs):
        self.layout = self._layout()
        self.app = self.create_app()

    def create_app(self):
        app = Application(
            layout=self.layout,
            key_bindings=self.kbindings(),
            full_screen=True,
            mouse_support=True,
            enable_page_navigation_bindings=True,
        )
        return app

    def kbindings(self):
        # Key bindings.
        kb = KeyBindings()
        # kb.add("tab")(focus_next)  # down
        # kb.add("s-tab")(focus_previous)  # up
        @kb.add("s-down")  # down
        def _(event):
            focus_next(event)
            # print(self.layout.current_control)

        @kb.add("s-up")  # up
        def _(event):
            focus_previous(event)

        # kb.add('escape')(lambda event: layout.focus(command_prompt))
        kb.add("c-q")(lambda event: get_app().exit())
        return kb

    def _help_message(self):
        return TopMessage(self)

    def _top(self):
        return Display(info_area)

    def _center(self):
        return ListView(list_buffer)

    def _botton(self):
        return CommandPrompt(command_buffer)

    def _layout(self):
        return Layout(
            HSplit([self._help_message(), self._top(), self._center(), self._botton()])
        )

    def run(self):
        self.app.run()


application = App()

from prompt_toolkit.application import Application

from radio.keybindings import main_kbindings
from radio.keybindings import prompt_kbindings

from radio.layout import layout

from radio.models import command_buffer
from radio.models import list_buffer
from radio.models import info_area

from radio.widgets import ListView
from radio.widgets import command_prompt

from radio.styles import style


list_view = ListView(list_buffer)
command_prompt = command_prompt(command_buffer, prompt_kbindings)


# Build a main application object.
application = Application(
    layout=layout(info_area, list_view, command_prompt),
    key_bindings=main_kbindings(),
    style=style,
    full_screen=True,
    mouse_support=True,
    enable_page_navigation_bindings=True,
)

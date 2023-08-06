from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.focus import focus_previous
from prompt_toolkit.application.current import get_app

from radio.commands import handle_command
from radio.models import command_buffer


def main_kbindings():
    # Key bindings.
    kb = KeyBindings()
    # kb.add("tab")(focus_next)  # down
    # kb.add("s-tab")(focus_previous)  # up
    kb.add("s-down")(focus_next)  # down
    kb.add("s-up")(focus_previous)  # up
    kb.add("c-q")(lambda event: get_app().exit())
    # kb.add('escape')(lambda event: layout.focus(command_prompt))
    return kb


def prompt_kbindings():

    kb = KeyBindings()

    @kb.add("enter")
    def _(event):
        handle_command(event)
        command_buffer.text = ""

    @kb.add("c-@")
    def _(event):
        print("aqui")

    return kb

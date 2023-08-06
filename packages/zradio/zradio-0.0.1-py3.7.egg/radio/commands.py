from radio.log import logger

from numbers import Number

from prompt_toolkit.contrib.regular_languages import compile
from prompt_toolkit.document import Document
from prompt_toolkit.application.current import get_app


from radio.models import list_buffer
from radio.models import radios
from radio.models import radio_browser
from radio.models import Radio
from radio.models import info_area

from radio.player import play_now
from radio.player import Player


COMMAND_GRAMMAR = compile(
    r"""(
        (?P<command>[^\s]+) \s+ (?P<subcommand>[^\s]+)  \s+  (?P<term>[^\s]+) |
        (?P<command>[^\s]+) \s+ (?P<term>[^\s]+) |
        (?P<command>[^\s!]+)
    )"""
)

COMMAND_TO_HANDLER = {}


def has_command_handler(command):
    return command in COMMAND_TO_HANDLER


def call_command_handler(command, **kwargs):
    COMMAND_TO_HANDLER[command](**kwargs)


def get_commands():
    return COMMAND_TO_HANDLER.keys()


def get_command_help(command):
    return COMMAND_TO_HANDLER[command].__doc__


def handle_command(event, **kwargs):
    logger.info(event.current_buffer.name)
    # logger.info(event.current_buffer.text)

    def is_help(text):
        if not text:
            return
        test = text.split("|")[0]
        test = test.replace(" ", "")
        return not test.isnumeric()

    if is_help(kwargs.get("text")):
        return  # TODO handle_help()

    # handle event of command_prompt (buffer)
    if event.current_buffer.name == "command_buffer":

        # !!!!! handle event of command_prompt (buffer)
        input_string = event.current_buffer.text

        match = COMMAND_GRAMMAR.match(input_string)

        if match is None:
            return

        # post process grammar
        variables = match.variables()

        command = variables.get("command")

        kwargs.update({"variables": variables, "event": event})
        if has_command_handler(command):
            call_command_handler(command, **kwargs)

    # handle event of list_view !!!!! (not buffer)
    if event.current_buffer.name == "list_buffer":
        call_command_handler("play", **kwargs)


def cmd(name):
    """
    Decorator to register commands in this namespace
    """

    def decorator(func):
        COMMAND_TO_HANDLER[name] = func

    return decorator


@cmd("exit")
def exit(**kwargs):
    """ exit Ctrl + Q"""
    get_app().exit()


@cmd("play")
def play(**kwargs):
    def get_playable_station():
        # TODO
        pass

    index = kwargs.get("index", None)
    # play from lits_view

    if isinstance(index, Number):
        obj = radios.get_obj(kwargs.get("index"))
    else:
        # play from command_prompt
        variables = kwargs.get("variables")
        command = "{}_{}".format("stations", variables.get("subcommand"))
        term = variables.get("term")
        data = getattr(radio_browser, command)(term)
        obj = Radio(**data[0])
    info_area.text = obj.id + " | > " + obj.name
    info_area.text += "\n\n\n" + obj.url
    play_now.put(obj)

    Player()
    logger.info("playing...")


@cmd("bytag")
def bytag(**kwargs):
    variables = kwargs.get("variables")
    term = variables.get("term")
    radios.data = radio_browser.stations_bytag(term)
    list_buffer.reset(Document(radios.content, 0))


@cmd("stations")
def stations(**kwargs):
    variables = kwargs.get("variables")
    command = "{}_{}".format(
        variables.get("command"), variables.get("subcommand")
    )
    term = variables.get("term")
    radios.data = getattr(radio_browser, command)(term)
    list_buffer.reset(Document(radios.content, 0))


@cmd("info")
def info(**kwargs):
    """ show info about station """
    pass


@cmd("help")
def help(**kwargs):
    """ show help """
    # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
    commands = """Command List\n
codecs
countries
languages
states
stations
stations bycodec <codec>
stations bycodecexact <codecexact>
stations bycountry <country>
stations bycountryexact <countryexact>
stations byid <id>
stations bylanguage <language>
stations bylanguageexact <languageexact>
stations byname <name>
stations bynameexact <nameexact>
stations bystate <state>
stations bystateexact <stateexact>
stations bytag <tag>
stations bytagexact <tag>
stations byuuid <uuid>
tags\n"""
    list_buffer.reset(Document(commands), 0)
    list_buffer._set_cursor_position(0)

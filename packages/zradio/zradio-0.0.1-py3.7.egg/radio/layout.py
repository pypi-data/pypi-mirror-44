from prompt_toolkit.layout import Layout
from prompt_toolkit.layout import HSplit
from prompt_toolkit.layout import VSplit

from prompt_toolkit.widgets import Box
from prompt_toolkit.widgets import Label
from prompt_toolkit.widgets import Frame


def layout(vtop, vmid, vbottom):
    """
    --------------------------------
    vtop => info_area


    --------------------------------
    vmid => list_view






    ---------------------------------
    vbottom => command_prompt
    ---------------------------------


    """
    l = Layout(
        container=HSplit(
            [
                Box(
                    Label(
                        text="Press `shift UP` or `shift Down` to move the focus; Press `Ctrl + Q` to quit."
                    ),
                    padding_left=2,
                ),
                Frame(
                    HSplit([Box(vtop, padding_top=2, padding_left=2)]),
                    height=10,
                ),
                Frame(vmid),
                vbottom,
            ],
            modal=True,
        ),
        focused_element=vbottom,
    )
    return l

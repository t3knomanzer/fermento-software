from gui.widgets.buttons import Button
from gui.core.colors import BLACK


class InvisibleCloseButton(Button):
    def __init__(self, writer):
        super().__init__(
            writer,
            0,
            0,
            width=0,
            height=0,
            fgcolor=BLACK,
            bgcolor=BLACK,
            textcolor=BLACK,
        )
        self.active = False

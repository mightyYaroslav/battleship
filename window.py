import curses
import curses.panel
from typing import Dict


class Window:

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 boxed: bool = False,
                 scrollable: bool = False,
                 title: str = None,
                 title_flags: int = 0
                 ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scrollable = scrollable
        self.boxed = boxed
        self.title = title

        self.window = curses.newwin(height, width, y, x)
        self.window.scrollok(scrollable)
        self.panel = curses.panel.new_panel(self.window)
        if boxed:
            self.window.box()
        if title is not None:
            self.window.addstr(title, title_flags)


class TitleWindow(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=0,
            y=0,
            width=dims["title"]["width"],
            height=dims["title"]["height"],
            title="The Battleship Game",
            title_flags=curses.A_BOLD and curses.A_BLINK
        )


class Subtitle1Window(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=0,
            y=dims["title"]["height"],
            width=dims["subtitle"]["width"],
            height=dims["subtitle"]["height"],
            title="P1"
        )


class Subtitle2Window(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=dims["subtitle"]["width"],
            y=dims["title"]["height"],
            width=dims["subtitle"]["width"],
            height=dims["subtitle"]["height"],
            title="P2"
        )


class Player1Window(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=0,
            y=dims["title"]["height"] + dims["subtitle"]["height"],
            width=dims["player"]["width"],
            height=dims["player"]["height"],
            boxed=True
        )


class Player2Window(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=dims["player"]["width"],
            y=dims["title"]["height"] + dims["subtitle"]["height"],
            width=dims["player"]["width"],
            height=dims["player"]["height"],
            boxed=True
        )


class HistoryWindow(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=0,
            y=dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"],
            width=dims["history"]["width"],
            height=dims["history"]["height"],
            title="History:\n"
        )


class CommandWindow(Window):
    def __init__(self, dims: Dict[str, Dict[str, int]]):
        super().__init__(
            x=0,
            y=dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"][
                "height"] +
              dims["history"]["height"],
            width=dims["command"]["width"],
            height=dims["command"]["height"]
        )
        self.window.addstr(1, 1, "Player 1 turn:")

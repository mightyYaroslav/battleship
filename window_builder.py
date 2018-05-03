import curses
import curses.panel
from abc import ABC, abstractmethod
from typing import Dict
from window import Window


class WindowBuilder(ABC):

    def __init__(self, dims: Dict[str, Dict[str, int]]):
        self.window = Window()
        self.dims = dims

    @abstractmethod
    def set_scales(self):
        pass

    @abstractmethod
    def set_scrollable(self):
        pass

    @abstractmethod
    def set_boxed(self):
        pass

    @abstractmethod
    def set_title(self):
        pass


class TitleBuilder(WindowBuilder):

    def set_scales(self):
        self.window.x = 0
        self.window.y = 0
        self.window.width = self.dims["title"]["width"]
        self.window.height = self.dims["title"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = False

    def set_title(self):
        self.window.title = "The Battleship Game"
        self.window.window.addstr(self.window.title, curses.A_BOLD and curses.A_BLINK)


class Subtitle1Builder(WindowBuilder):

    def set_scales(self):
        self.window.x = 0
        self.window.y = self.dims["title"]["height"]
        self.window.width = self.dims["subtitle"]["width"]
        self.window.height = self.dims["subtitle"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = False

    def set_title(self):
        self.window.title = "P1"
        self.window.window.addstr(self.window.title)


class Subtitle2Builder(WindowBuilder):

    def set_scales(self):
        self.window.x = self.dims["subtitle"]["width"]
        self.window.y = self.dims["title"]["height"]
        self.window.width = self.dims["subtitle"]["width"]
        self.window.height = self.dims["subtitle"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = False

    def set_title(self):
        self.window.title = "P2"
        self.window.window.addstr(self.window.title)


class Player1Builder(WindowBuilder):

    def set_scales(self):
        self.window.x = 0
        self.window.y = self.dims["title"]["height"] + self.dims["subtitle"]["height"]
        self.window.width = self.dims["player"]["width"]
        self.window.height = self.dims["player"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = True
        self.window.window.box()

    def set_title(self):
        self.window.title = None


class Player2Builder(WindowBuilder):

    def set_scales(self):
        self.window.x = self.dims["player"]["width"]
        self.window.y = self.dims["title"]["height"] + self.dims["subtitle"]["height"]
        self.window.width = self.dims["player"]["width"]
        self.window.height = self.dims["player"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = True
        self.window.window.box()

    def set_title(self):
        self.window.title = None


class HistoryBuilder(WindowBuilder):
    def set_scales(self):
        self.window.x = 0
        self.window.y = self.dims["title"]["height"] + self.dims["subtitle"]["height"] + \
                        self.dims["title"]["height"] + self.dims["player"]["height"]

        self.window.width = self.dims["history"]["width"]
        self.window.height = self.dims["history"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = False

    def set_title(self):
        self.window.title = "History:\n"
        self.window.window.addstr(self.window.title)


class CommandBuilder(WindowBuilder):

    def set_scales(self):
        self.window.x = 0
        self.window.y = self.dims["title"]["height"] + \
                        self.dims["subtitle"]["height"] + self.dims["title"]["height"] + \
                        self.dims["player"]["height"] + self.dims["history"]["height"]

        self.window.width = self.dims["command"]["width"]
        self.window.height = self.dims["command"]["height"]
        self.window.window = curses.newwin(self.window.height, self.window.width, self.window.y, self.window.x)
        self.window.panel = curses.panel.new_panel(self.window.window)
        self.window.window.addstr(1, 1, "Player 1 turn:")

    def set_scrollable(self):
        self.window.scrollable = False

    def set_boxed(self):
        self.window.boxed = False

    def set_title(self):
        self.window.title = None


class WindowManager:

    def __init__(self, builder: WindowBuilder):
        self.builder = builder

    def build(self) -> Window:
        self.builder.set_scales()
        self.builder.set_scrollable()
        self.builder.set_boxed()
        self.builder.set_title()
        return self.builder.window

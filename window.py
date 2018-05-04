import curses
import curses.panel


class Window:

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            width: int = 0,
            height: int = 0,
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
        self.title_flags = title_flags

        self.window = curses.newwin(height, width, y, x)
        self.window.scrollok(scrollable)
        self.panel = curses.panel.new_panel(self.window)
        if boxed:
            self.window.box()
        if title is not None:
            self.window.addstr(title, title_flags)

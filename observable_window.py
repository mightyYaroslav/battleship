import curses
import curses.panel
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict

from observable import Observable


class ObservableWindow:

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
        self.x = Observable(x, lambda new_x: self._update_window(x=new_x))
        self.y = Observable(y, lambda new_y: self._update_window(y=new_y))
        self.width = Observable(width, lambda new_width: self._update_window(width=new_width))
        self.height = Observable(height, lambda new_height: self._update_window(height=new_height))
        self.scrollable = Observable(scrollable, self._update_scrollable)
        self.boxed = Observable(boxed, self._update_boxed)
        self.title = Observable(title, lambda new_title: self._update_title(title=new_title))
        self.title_flags = Observable(title_flags, lambda new_flags: self._update_title(title_flags=new_flags))

        self.window = curses.newwin(height, width, y, x)
        self.window.scrollok(scrollable)
        self.panel = curses.panel.new_panel(self.window)
        if boxed:
            self.window.box()
        if title is not None:
            self.window.addstr(title, title_flags)

    def _update_window(self, x: int = None, y: int = None, width: int = None, height: int = None):
        if x is None:
            x = self.x.data
        if y is None:
            y = self.y.data
        if width is None:
            width = self.width.data
        if height is None:
            height = self.height.data
        self.window = curses.newwin(height, width, y, x)
        self.window.scrollok(self.scrollable.data)
        self.panel = curses.panel.new_panel(self.window.data)
        if self.boxed:
            self.window.box()
        if self.title is not None:
            self.window.addstr(self.title.data, self.title_flags.data)

    def _update_title(self, title: str = None, title_flags: int = None):
        if title is None:
            title = self.title.data
        if title_flags is None:
            title_flags = self.title_flags
        if title is not None:
            self.window.addstr(title, title_flags)

    def _update_scrollable(self, scrollable: bool):
        self.window.scrollok(scrollable)

    def _update_boxed(self, boxed: bool):
        if boxed:
            self.window.box()

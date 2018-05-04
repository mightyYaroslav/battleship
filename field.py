from enum import Enum
from typing import Any

from ship import Ship
from point import Point
from symbol_point import SymbolPoint, PointSymbol


class Field:
    def __init__(self, rows: int, cols: int, symbol: str = "-"):
        self.rows = rows
        self.cols = cols
        self.symbol = symbol
        self.ships = []
        self._points = set()

    def add_ship(self, s: Ship):
        self.ships.append(s)

    def remove_ship(self, s: Ship) -> bool:
        if s not in self.ships:
            return False
        self.ships.remove(s)
        return True

    def launch(self, p: Point) -> bool:
        for pt in self._points:
            if p == pt and pt.state.char == PointSymbol.KILL.value:
                return False
        for ship in self.ships:
            if p in ship:
                sym_p = SymbolPoint(p)
                sym_p.kill()
                self._points.add(sym_p)
                return True
        sym_p = SymbolPoint(p)
        sym_p.miss()
        self._points.add(sym_p)
        return False

    def add_coordinates(self, window: Any):
        for j in range(10):
            window.addstr(j, 4, chr(ord('A') + j + 3))

        for i in range(10):
            window.addstr(4, i, str(i + 3))

    def erase(self, window: Any):
        for i in range(10):
            for j in range(10):
                window.addstr(j, i, "-")

    def put_points(self, window: Any):
        for p in self._points:
            window.addstr(p.y, p.x, p.state.char)

    def put_ships(self, window: Any):
        for ship in self.ships:
            for i in range(ship.start.x, ship.end.x + 1):
                for j in range(ship.start.y, ship.end.y + 1):
                    window.addstr(j, i, ship.symbol)

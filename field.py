from functools import reduce
from typing import Any

from ship import Ship
from point import Point


class Field:
    def __init__(self, rows: int, cols: int, symbol: str = "-"):
        self.rows = rows
        self.cols = cols
        self.symbol = symbol
        self.ships = []
        self._kill_points = set()
        self._miss_points = set()

    def add_ship(self, s: Ship):
        self.ships.append(s)

    def miss_points_str(self) -> str:
        return " ".join(self._miss_points)

    def kill_points_str(self) -> str:
        return " ".join(self._kill_points)

    def remove_ship(self, s: Ship) -> bool:
        if s not in self.ships:
            return False
        self.ships.remove(s)
        return True

    def launch(self, p: Point) -> bool:
        if p in self._kill_points:
            return False
        for ship in self.ships:
            if p in ship:
                self._kill_points.add(p)
                return True
        self._miss_points.add(p)
        return False

    def add_coordinates(self, window: Any, max_width: int, max_height: int):
        for j in range(round(max_height / 4) - 5, round(max_height / 4) + 5):
            window.addstr(j, round(max_width / 4) - 6, chr(ord('A') + j - round(max_height / 4) + 5))

        for i in range(round(max_width / 4) - 5, round(max_width / 4) + 5):
            window.addstr(round(max_height / 4) - 6, i, str(i - round(max_width / 4) + 5))

    def erase(self, window: Any, max_width: int, max_height: int):
        for i in range(round(max_width / 4) - 5, round(max_width / 4) + 5):
            for j in range(round(max_height / 4) - 5, round(max_height / 4) + 5):
                window.addstr(j, i, "-")

    def put_kill_points(self, window: Any, max_width: int, max_height: int):
        for p in self._kill_points:
            window.addstr(round(max_height / 2) - 5 + p.y, round(max_width / 2) - 5 + p.x, "K")

    def put_miss_points(self, window: Any, max_width: int, max_height: int):
        for p in self._miss_points:
            window.addstr(round(max_height / 2) - 5 + p.y, round(max_width / 2) - 5 + p.x, "M")

    def put_ships(self, window: Any, max_width: int, max_height: int):
        for ship in self.ships:
            if ship.start.x == ship.end.x:
                for j in range(ship.start.y, ship.end.y + 1):
                    window.addstr(round(max_height / 4) - 5 + j, round(max_width / 4) - 5 + ship.start.x, ship.symbol)
            else:
                for i in range(ship.start.x, ship.end.x + 1):
                    window.addstr(round(max_height / 4) - 5 + ship.start.y, round(max_width / 4) - 5 + i, ship.symbol)

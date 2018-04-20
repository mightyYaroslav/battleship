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
        self._kill_points = []
        self._miss_points = []

    def add_ship(self, s: Ship):
        self.ships.append(s)

    def miss_points_str(self) -> str:
        return reduce(lambda a, x: a + str(x) + " ", self._miss_points, "")

    def kill_points_str(self) -> str:
        return reduce(lambda a, x: a + str(x) + " ", self._kill_points, "")

    def remove_ship(self, s: Ship) -> bool:
        if s not in self.ships:
            return False
        self.ships.remove(s)
        return True

    def launch(self, i: int, j: int) -> bool:
        for ship in self.ships:
            if ship.contains(Point(i, j)):
                self._kill_points.append(Point(i, j))
                return True
        self._miss_points.append(Point(i, j))
        return False

    def add_coordinates(self, window: Any, max_width: int, max_height: int):
        for j in range(max_height // 4 - 5, max_height // 4 + 5):
            window.addstr(j, max_width // 4 - 6, chr(ord('A') + j - max_height // 4 + 5))

        for i in range(max_width // 4 - 5, max_width // 4 + 5):
            window.addstr(max_height // 4 - 6, i, str(i - max_width // 4 + 5))

    def put_empty(self, window: Any, max_width: int, max_height: int):
        for i in range(max_width // 4 - 5, max_width // 4 + 5):
            for j in range(max_height // 4 - 5, max_height // 4 + 5):
                window.addstr(j, i, "-")

    def put_kill_points(self, window: Any):
        for p in self._kill_points:
            window.addstr(p.y, p.x, "K")

    def put_miss_points(self, window: Any):
        for p in self._miss_points:
            window.addstr(p.y, p.x, "M")

    def put_ships(self, window: Any):
        for ship in self.ships:
            if ship.start.x == ship.end.x:
                for j in range(ship.start.y, ship.end.y):
                    window.addstr(j, ship.start.x, ship.symbol)
            else:
                for i in range(ship.start.x, ship.end.x):
                    window.addstr(ship.start.y, i, ship.symbol)

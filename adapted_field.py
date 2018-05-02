from field import Field
from typing import Any

from point import Point
from ship import Ship
from symbol_point import SymbolPoint


class AdaptedField(Field):
    def __init__(self, field: Field):
        super().__init__(field.rows, field.cols, field.symbol)
        self.field = field
        for p in field._points:
            pass

    def add_coordinates(self, window: Any, max_width: int, max_height: int):
        for j in range(round(max_height / 4) - 5, round(max_height / 4) + 5):
            window.addstr(j, round(max_width / 4) - 6, chr(ord('A') + j - round(max_height / 4) + 5))

        for i in range(round(max_width / 4) - 5, round(max_width / 4) + 5):
            window.addstr(round(max_height / 4) - 6, i, str(i - round(max_width / 4) + 5))

    def erase(self, window: Any, max_width: int, max_height: int):
        for i in range(round(max_width / 4) - 5, round(max_width / 4) + 5):
            for j in range(round(max_height / 4) - 5, round(max_height / 4) + 5):
                window.addstr(j, i, "-")

    def put_points(self, window: Any, max_width: int, max_height: int):
        for p in self.field._points:
            self._points.add(SymbolPoint(Point(x=p.x + round(max_width / 2) - 5, y=p.y + round(max_height / 2) - 5), p.symbol))
        super().put_points(window, max_width, max_height)

    def put_kill_points(self, window: Any, max_width: int, max_height: int):
        for p in self.field._kill_points:
            self._kill_points.add(Point(x=p.x + round(max_width / 2) - 5, y=p.y + round(max_height / 2) - 5))
        super().put_kill_points(window, max_width, max_height)

    def put_miss_points(self, window: Any, max_width: int, max_height: int):
        for i in self.field._miss_points:
            self._miss_points.add(Point(x=p.x + round(max_width / 2) - 5, y=p.y + round(max_height / 2) - 5))
        super().put_miss_points(window, max_width, max_height)

    def put_ships(self, window: Any, max_width: int, max_height: int):
        for s in self.field.ships:
            new_ship = Ship(
                start=Point(
                    x=s.start.x + round(max_width / 4) - 5,
                    y=s.start.y + round(max_height / 4) - 5
                ),
                end=Point(
                    x=s.end.x + round(max_width / 4) - 5,
                    y=s.end.y + round(max_height / 4) - 5
                )
            )
            self.ships.append(new_ship)
        super().put_ships(window, max_width, max_height)

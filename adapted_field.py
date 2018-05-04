from field import Field
from typing import Any

from point import Point
from ship import Ship
from symbol_point import SymbolPoint, MissedState


class AdaptedField(Field):
    def __init__(self, field: Field, max_width: int, max_height: int):
        super().__init__(field.rows, field.cols, field.symbol)
        self.field = field
        self.max_width = max_width
        self.max_height = max_height
        for p in self.field._points:
            self._points.add(
                SymbolPoint(
                    Point(
                        x=p.x + round(self.max_width / 2) - 5,
                        y=p.y + round(self.max_height / 2) - 5),
                    p.state
                )
            )

        for s in self.field.ships:
            new_ship = Ship(
                start=Point(
                    x=s.start.x + round(self.max_width / 4) - 5,
                    y=s.start.y + round(self.max_height / 4) - 5
                ),
                end=Point(
                    x=s.end.x + round(self.max_width / 4) - 5,
                    y=s.end.y + round(self.max_height / 4) - 5
                )
            )
            self.ships.append(new_ship)

    def add_coordinates(self, window: Any):
        for j in range(round(self.max_height / 4) - 5, round(self.max_height / 4) + 5):
            window.addstr(j, round(self.max_width / 4) - 6, chr(ord('A') + j - round(self.max_height / 4) + 5))

        for i in range(round(self.max_width / 4) - 5, round(self.max_width / 4) + 5):
            window.addstr(round(self.max_height / 4) - 6, i, str(i - round(self.max_width / 4) + 5))

    def erase(self, window: Any):
        for i in range(round(self.max_width / 4) - 5, round(self.max_width / 4) + 5):
            for j in range(round(self.max_height / 4) - 5, round(self.max_height / 4) + 5):
                window.addstr(j, i, "-")

import curses
from typing import Any

from field import Field
from point import Point
from ship import Ship
from window import Window


class Player:
    def __init__(self, name: str, window: Window = None):
        self.name = name
        self.field = Field(10, 10)
        self.window = window
        self.score = 0

    def setup(
            self,
            screen: Any,
            max_y: int,
            max_x: int,
            min_y: int,
            min_x: int
    ):
        ship_size = 1
        i = 0
        ship_pts = []
        vert = True

        f_x = round((max_x + min_x) / 2) - 5
        f_y = round((max_y + min_y) / 2) - 5

        while True:
            if len(ship_pts) == ship_size:
                xs = [pt.x for pt in ship_pts]
                ys = [pt.y for pt in ship_pts]
                self.field.add_ship(Ship(Point(min(xs), min(ys)), Point(max(xs), max(ys))))
                ship_pts = []
                i += 1
                if i == 5:
                    break
                elif i == 5 + 1 - ship_size:
                    ship_size -= 1
                    i = 0

            e = screen.getch()
            if e == ord('q'):
                break
            if e == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                if min_x <= mx <= max_x and min_y <= my <= max_y:
                    if len(ship_pts) == 0:
                        screen.addstr(my, mx, "x")
                        ship_pts.append(Point(int(mx - f_x), int(my - f_y)))

                    if len(ship_pts) == 1 and \
                            ((abs(ship_pts[0].x + f_x - mx) == 1 and ship_pts[0].y + f_y == my) or
                             (abs(ship_pts[0].y + f_y - my) == 1 and ship_pts[0].x + f_x == mx)):
                        vert = (abs(ship_pts[0].x + f_x - mx) == 1 and ship_pts[0].y + f_y == my)
                        screen.addstr(my, mx, "x")
                        ship_pts.append(Point(int(mx - f_x), int(my - f_y)))

                    for pt in ship_pts:
                        if (vert and (abs(pt.x + f_x - mx) == 1 and pt.y + f_y == my)) or \
                                (not vert and (abs(pt.y + f_y - my) == 1 and pt.x + f_x == mx)):
                            screen.addstr(my, mx, "x")
                            ship_pts.append(Point(int(mx - f_x), int(my - f_y)))
                            break

    def launch(self, point: Point, player):
        gotcha = player.field.launch(point)
        if gotcha:
            self.score += 1

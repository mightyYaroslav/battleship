from ship import Ship
from point import Point


class Field:
    def __init__(self, rows: int, cols: int, symbol: str = "-"):
        self.rows = rows
        self.cols = cols
        self.symbol = symbol
        self.ships = []

    def add_ship(self, s: Ship):
        self.ships.append(s)

    # curses.initscr()

    def remove_ship(self, s: Ship) -> bool:
        if s not in self.ships:
            return False
        self.ships.remove(s)
        return True

    def launch(self, i: int, j: int) -> bool:
        for ship in self.ships:
            if ship.contains(Point(i, j)):
                return True
        return False

    def add_coordinates(self, window, max_width, max_height):
        for j in range(max_height // 4 - 5, max_height // 4 + 5):
            window.addstr(j, max_width // 4 - 6, chr(ord('A') + j - max_height // 4 + 5))

        for i in range(max_width // 4 - 5, max_width // 4 + 5):
            window.addstr(max_height // 4 - 6, i, str(i - max_width // 4 + 5))

    def put_empty(self, window, max_width, max_height):
        for i in range(max_width // 4 - 5, max_width // 4 + 5):
            for j in range(max_height // 4 - 5, max_height // 4 + 5):
                window.addstr(j, i, "-")

    def put_ships(self, window):
        for ship in self.ships:
            if ship.start.x == ship.end.x:
                for j in range(ship.start.y, ship.end.y):
                    window.addstr(j, ship.start.x, ship.symbol)
            else:
                for i in range(ship.start.x, ship.end.x):
                    window.addstr(ship.start.y, i, ship.symbol)

from ship import Ship


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

    def __str__(self):
        strs = [[self.symbol for _ in range(self.cols)] for _ in range(self.rows)]
        for ship in self.ships:
            if ship.start.x == ship.end.x:
                for j in range(ship.start.y, ship.end.y):
                    strs[ship.start.x][j] = ship.symbol
                else:
                    for i in range(ship.start.x, ship.end.x):
                        strs[i][ship.start.y] = ship.symbol
        return "\n".join(["".join(s) for s in strs])

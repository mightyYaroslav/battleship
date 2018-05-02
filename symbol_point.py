from point import Point


class SymbolPoint(Point):

    def __init__(self, p: Point, symbol: str = '-'):
        super().__init__(p.x, p.y)
        self.symbol = symbol

from point import Point


class Ship:
    def __init__(self, start: Point = Point(0, 0), end: Point = Point(0, 0), symbol='x'):
        self.start = start if start <= end else end
        self.end = end if start <= end else start
        self.symbol = symbol

    def contains(self, point: Point) -> bool:
        return self.start <= point <= self.end

    def __str__(self):
        return "start: " + str(self.start) + " end: " + str(self.end)

from field import Field
from point import Point


class Player:
    def __init__(self, name: str, field: Field = None):
        self.name = name
        self.field = field
        self._score = 0

    def launch(self, point: Point, player) -> bool:
        for ship in player.field.ships:
            if ship.contains(point):
                print("Gotcha")
                return True
        return False

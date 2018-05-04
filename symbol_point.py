from abc import abstractmethod, ABC
from enum import Enum

from point import Point


class PointSymbol(Enum):
    KILL = "K"
    MISS = "M"


class PointState(ABC):
    @property
    @abstractmethod
    def char(self):
        pass


class MissedState(PointState):
    @property
    def char(self):
        return PointSymbol.MISS.value


class KilledState(PointState):
    @property
    def char(self):
        return PointSymbol.KILL.value


class SymbolPoint(Point):
    _missed_state = MissedState()
    _killed_state = KilledState()

    def __init__(self, p: Point, state: PointState = None):
        super().__init__(p.x, p.y)
        self.p = p
        if state is None:
            self.state = SymbolPoint._missed_state
        else:
            self.state = state

    def miss(self):
        self.state = SymbolPoint._missed_state

    def kill(self):
        self.state = SymbolPoint._killed_state

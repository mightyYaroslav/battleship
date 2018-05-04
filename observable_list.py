from typing import List, Any


class ObservableList(list):

    def __init__(self, arr: List[Any]):
        super().__init__()
        self.list = arr
        self.callbacks = []

    def subscribe(self, cb):
        self.callbacks.append(cb)

    def unsubscribe(self, cb):
        self.callbacks.remove(cb)

    def _notify(self, change):
        for f in self.callbacks:
            f(self.list, change)

    def append(self, obj):
        super().append(obj)
        self._notify([obj])

    def __add__(self, other):
        super().__add__(other)
        self._notify(other)


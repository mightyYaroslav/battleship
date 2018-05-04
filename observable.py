from typing import Any, List


class Observable:
    def __init__(self, o: Any, callback):
        self.callback = callback
        self._o = o

    def notify(self):
        self.callback(self._o)
        # for fn in self.callbacks:
        #     fn(self._o)

    @property
    def data(self):
        return self._o

    @data.setter
    def data(self, val: Any):
        self._o = val
        self.notify()

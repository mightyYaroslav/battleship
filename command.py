from abc import ABC, abstractmethod

from point import Point


class Command:

    def __init__(self, binput: bytes):
        self.binput = binput
        self.str = binput.decode("utf-8")

    def point(self) -> Point:
        x = int(self.str[1])
        y = ord(self.str[0].lower()) - ord('a')
        return Point(x, y)


class ValidatedCommand(Command):

    def __init__(self, cmd: Command):
        super().__init__(cmd.binput)
        self.cmd = cmd

    def validate(self) -> bool:
        return isinstance(self.str, str) and \
               len(self.str) == 2 and \
               ord('a') <= ord(self.str[0].lower()) <= ord('j') and \
               self.str[1].isnumeric()

    def point(self):
        if self.validate():
            return super().point()

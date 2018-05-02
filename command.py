from abc import ABC, abstractmethod

from point import Point


class Command:

    @staticmethod
    def point(binput: bytes) -> Point:
        command = binput.decode("utf-8")
        x = int(command[1])
        y = ord(command[0].lower()) - ord('a')
        return Point(x, y)

    @staticmethod
    def validate(cmd: str) -> bool:
        return isinstance(cmd, str) and \
               len(cmd) == 2 and \
               ord('a') <= ord(cmd[0].lower()) <= ord('j') and \
               cmd[1].isnumeric()

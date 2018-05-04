import curses
from game import Game


def main(screen):
    game = Game(screen)
    game.setup()
    game.play()
    game.result()


try:
    curses.wrapper(main)
except KeyboardInterrupt as e:
    print("Exit")

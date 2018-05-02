import curses
import curses.panel
import time
from typing import Any, Dict, Tuple

from adapted_field import AdaptedField
from command import Command
from dimensions import Dimensions
from player import Player
from window import TitleWindow, Subtitle1Window, Subtitle2Window, Player1Window, Player2Window, HistoryWindow, \
    CommandWindow, Window


class Game:
    class __Game:
        def __init__(self, screen: Any):
            self.screen = screen
            self.max_height, self.max_width = screen.getmaxyx()
            self.dims = Dimensions.for_game(self.max_height, self.max_width)
            self.players = (Player("P1", Player1Window(self.dims)), Player("P2", Player2Window(self.dims)))
            self.turn = 0

    instance = None

    def __init__(self, screen: Any):
        if Game.instance is None:
            Game.instance = Game.__Game(screen)

    def setup(self):
        players, screen, dims = self.instance.players, self.instance.screen, self.instance.dims
        max_width, max_height = self.instance.max_width, self.instance.max_height

        title = TitleWindow(dims)
        subtitle1, subtitle2 = Subtitle1Window(self.instance.dims), Subtitle2Window(self.instance.dims)

        for player in players:
            player.field.erase(player.window.window, max_width, max_height)
            player.field.add_coordinates(player.window.window, max_width, max_height)

        curses.mousemask(True)
        curses.curs_set(False)
        curses.noecho()

        curses.panel.update_panels()
        curses.doupdate()

        players[0].setup(
            screen,
            round(dims["player"]["height"] / 2) + 6,
            round(dims["player"]["width"] / 2) + 4,
            round(dims["player"]["height"] / 2) - 3,
            round(dims["player"]["width"] / 2) - 5
        )

        players[0].field.erase(players[0].window.window, max_width, max_height)
        players[0].field.add_coordinates(players[0].window.window, max_width, max_height)

        curses.panel.update_panels()
        curses.doupdate()

        players[1].setup(
            screen,
            round(dims["player"]["height"] / 2) + 6,
            round(dims["player"]["width"] / 2 * 3) * 3 + 4,
            round(dims["player"]["height"] / 2) - 3,
            round(dims["player"]["width"] / 2 * 3) - 5
        )

        players[1].field.erase(players[1].window.window, max_width, max_height)
        players[1].field.add_coordinates(players[1].window.window, max_width, max_height)
        curses.panel.update_panels()
        curses.doupdate()

        curses.mousemask(False)

    def command_warn(self, cmd: Window):
        cmd.window.move(2, 1)
        cmd.window.addstr("Input is incorrect!")
        cmd.window.refresh()
        time.sleep(1)
        cmd.window.move(2, 1)
        cmd.window.clrtoeol()

    def game_loop(
            self,
            cmd: Window,
            history: Window
    ):
        players, dims, turn = self.instance.players, self.instance.dims, self.instance.turn
        max_width, max_height = self.instance.max_width, self.instance.max_height

        while True:
            player = players[turn]
            enemy = players[0 if turn == 1 else 1]

            AdaptedField(enemy.field).erase(enemy.window.window, max_width, max_height)
            AdaptedField(player.field).erase(player.window.window, max_width, max_height)
            # AdaptedField(player.field).put_ships(player.window.window, max_width, max_height)

            cmd.window.move(2, 1)
            binput = cmd.window.getstr()

            if len(binput) == 0:
                break
            if not Command.validate(binput.decode("utf-8")):
                self.command_warn(cmd)
                continue
            cmd.window.move(2, 1)

            history.window.addstr("P" + str(turn + 1) + ": " + binput.decode("utf-8") + "\n")
            player.launch(Command.point(binput), enemy)
            AdaptedField(enemy.field).put_points(enemy.window.window, dims["player"]["width"], dims["player"]["height"])

            if players[0].score == 15 or players[1].score == 15:
                break

            curses.panel.update_panels()
            curses.doupdate()
            turn = 1 if turn == 0 else 0
            cmd.window.clrtoeol()
            cmd.window.addstr(1, 1, "Player " + str(turn + 1) + " turn:")

    def play(self):
        dims = self.instance.dims
        history = HistoryWindow(dims)
        cmd = CommandWindow(dims)

        curses.panel.update_panels()
        curses.doupdate()

        curses.echo()
        curses.curs_set(True)

        self.game_loop(cmd, history)

    def result(self):
        players, screen = self.instance.players, self.instance.screen
        max_width, max_height = self.instance.max_width, self.instance.max_height
        screen.clear()
        screen.refresh()
        curses.curs_set(False)
        if players[0].score == players[1].score:
            result = "Draw!"
        elif players[0].score > players[1].score:
            result = "Player 1 wins!"
        else:
            result = "Player 2 wins!"
        screen.addstr(0, 0, result)
        screen.addstr(1, 0, "P1 Score: " + str(players[0].score) + "\n")
        screen.addstr(2, 0, "P2 Score: " + str(players[1].score) + "\n")
        screen.addstr("\n".join([str(sh) for sh in players[0].field.ships]) + "\n\n\n")
        screen.addstr("\n".join([str(sh) for sh in players[1].field.ships]) + "\n")
        screen.addstr("Screen bounds: " + "\n")
        screen.addstr("Width: " + str(max_width) + "\n")
        screen.addstr("Height: " + str(max_height) + "\n")
        screen.getch()

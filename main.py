import time
from functools import reduce
from typing import Dict

from field import Field
from ship import Ship
from point import Point
from player import Player

# f = Field(10, 10)
# print(f)
# print('\n')
# f.add_ship(Ship(Point(1,1), Point(1,3)))
# player1=Player(name="yaroslav", field=f)
# player2 = Player(name="lera")
# print(player2.launch(Point(1,4), player1))
# идея: использовать стейт для точки, стейт для корабля, обсервер для наблюдения за изменениями , декоратор для создания точки со стейтом, класс игры как синглтон
# для сохранения данных использовать историю, а ввод комманд обрабатывать шаблоном "комманда"
# Видимость полей контролируется с помощью прокси


import curses
import curses.panel
import signal


def validate_command(cmd: str) -> bool:
    return isinstance(cmd, str) and len(cmd) == 2 and ord('a') <= ord(cmd[0]) <= ord('j') and cmd[1].isnumeric()


def dims_for_game(max_height: int, max_width: int) -> Dict[str, Dict[str, int]]:
    dims = {
        "title": {
            "width": max_width,
            "height": 1
        },
        "subtitle": {
            "width": max_width // 2,
            "height": 1
        },
        "player": {
            "width": max_width // 2,
            "height": max_height // 2
        },
        "history": {
            "width": max_width
        },
        "command": {
            "width": max_width,
            "height": 4
        }
    }

    sumheight = 0
    for v in dims.values():
        for (dim_key, dim_val) in v.items():
            if dim_key == "height":
                sumheight += dim_val

    dims["history"]["height"] = max_height - sumheight

    return dims


def get_title_panel(dims):
    title_window = curses.newwin(
        dims["title"]["height"],
        dims["title"]["width"],
        0,
        0
    )
    title_panel = curses.panel.new_panel(title_window)
    title_window.addstr("The Battleship Game", curses.A_BOLD and curses.A_BLINK)
    return title_panel


def get_subtitle_panels(dims):
    subtitle1_window = curses.newwin(
        dims["subtitle"]["height"],
        dims["subtitle"]["width"],
        dims["title"]["height"],
        0
    )
    subtitle1_panel = curses.panel.new_panel(subtitle1_window)
    subtitle1_window.addstr("P1")

    subtitle2_window = curses.newwin(
        dims["subtitle"]["height"],
        dims["subtitle"]["width"],
        dims["title"]["height"],
        dims["subtitle"]["width"])
    subtitle2_panel = curses.panel.new_panel(subtitle2_window)
    subtitle2_window.addstr("P2")
    return (subtitle1_panel, subtitle2_panel)


def get_player_panels(dims, max_height, max_width):
    p1_window = curses.newwin(
        dims["player"]["height"],
        dims["player"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"],
        0
    )
    p1_window.box()
    p1_panel = curses.panel.new_panel(p1_window)

    p2_window = curses.newwin(
        dims["player"]["height"],
        dims["player"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"],
        dims["player"]["width"]
    )
    p2_window.box()
    p2_panel = curses.panel.new_panel(p2_window)

    init_player_window(p1_window, max_height, max_width)
    init_player_window(p2_window, max_height, max_width)
    return (p1_window, p1_panel, p2_window, p2_panel)


def init_player_window(window, max_height: int, max_width: int):
    for i in range(max_width // 4 - 5, max_width // 4 + 5):
        for j in range(max_height // 4 - 5, max_height // 4 + 5):
            window.addstr(j, i, "-")

    for j in range(max_height // 4 - 5, max_height // 4 + 5):
        window.addstr(j, max_width // 4 - 6, chr(ord('A') + j - max_height // 4 + 5))

    for i in range(max_width // 4 - 5, max_width // 4 + 5):
        window.addstr(max_height // 4 - 6, i, str(i - max_width // 4 + 5))


def get_history_panel(dims):
    history_pad = curses.newpad(
        dims["history"]["height"],
        dims["history"]["width"]
    )

    history_window = curses.newwin(
        dims["history"]["height"],
        dims["history"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"],
        0
    )
    history_window.scrollok(True)
    history_panel = curses.panel.new_panel(history_window)

    history_window.addstr("History:\n")
    return (history_window, history_panel)


def get_command_panel(dims):
    cmd_window = curses.newwin(
        dims["command"]["height"],
        dims["command"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"] +
        dims["history"]["height"],
        0
    )
    cmd_window.box()
    cmd_panel = curses.panel.new_panel(cmd_window)

    cmd_window.addstr(1, 1, "Player 1 turn:")
    return (cmd_window, cmd_panel)


def game_loop(command_window, history_window):
    player1_turn = True
    while True:
        command_window.move(2, 1)
        key = command_window.getstr()
        if len(key) == 0:
            # screen.clear()
            # screen.refresh()
            break
        if not validate_command(key.decode("utf-8")):
            command_window.move(2, 1)
            command_window.addstr("Input is incorrect!")
            command_window.refresh()
            time.sleep(1)
            command_window.move(2, 1)
            command_window.clrtoeol()
            continue
        command_window.move(2, 1)
        history_window.addstr(("P1: " if player1_turn else "P2: ") + key.decode("utf-8") + "\n")

        curses.panel.update_panels()
        curses.doupdate()
        player1_turn = not player1_turn
        command_window.clrtoeol()
        command_window.addstr(1, 1, "Player " + ("1" if player1_turn else "2") + " turn:")


def setup_loop(screen):
    while True:
        e = screen.getch()
        if e == ord("q"):
            break
        if e == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            y, x = screen.getyx()
            screen.addstr(my, mx, "x")
            # player_window.refresh()


def main(screen):
    max_height, max_width = screen.getmaxyx()

    dims = dims_for_game(max_height, max_width)

    # Setup

    # Title window
    title_panel = get_title_panel(dims)

    # Subtitle windows
    subtitle1_panel, subtitle2_panel = get_subtitle_panels(dims)

    # Player windows
    player1_window, player1_panel, player2_window, player2_panel = get_player_panels(dims, max_height, max_width)

    curses.mousemask(True)
    curses.curs_set(False)
    curses.noecho()

    curses.panel.update_panels()
    curses.doupdate()

    setup_loop(screen)
    setup_loop(screen)

    curses.mousemask(False)

    # Game

    # History window
    history_window, history_panel = get_history_panel(dims)

    # Command window
    cmd_window, cmd_panel = get_command_panel(dims)

    curses.panel.update_panels()
    curses.doupdate()

    curses.echo()
    curses.curs_set(True)

    game_loop(cmd_window, history_window)


try:
    curses.wrapper(main)
except KeyboardInterrupt as e:
    print("Exit")

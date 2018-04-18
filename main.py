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


def get_title_panel(lines: int, cols: int, y: int, x: int):
    title_window = curses.newwin(
        lines,
        cols,
        y,
        x
    )
    title_panel = curses.panel.new_panel(title_window)
    title_window.addstr("The Battleship Game", curses.A_BOLD and curses.A_BLINK)
    return title_panel


def get_subtitle_panels(dims):
    sub_title_window1 = curses.newwin(
        dims["subtitle"]["height"],
        dims["subtitle"]["width"],
        dims["title"]["height"],
        0
    )
    sub_title_panel1 = curses.panel.new_panel(sub_title_window1)
    sub_title_window1.addstr("P1")

    sub_title_window2 = curses.newwin(
        dims["subtitle"]["height"],
        dims["subtitle"]["width"],
        dims["title"]["height"],
        dims["subtitle"]["width"])
    sub_title_panel2 = curses.panel.new_panel(sub_title_window2)
    sub_title_window2.addstr("P2")
    return (sub_title_panel1, sub_title_panel2)


def get_player_panels(dims, max_height, max_width):
    subwindow1 = curses.newwin(
        dims["player"]["height"],
        dims["player"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"],
        0
    )
    subwindow1.box()
    panel1 = curses.panel.new_panel(subwindow1)

    subwindow2 = curses.newwin(
        dims["player"]["height"],
        dims["player"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"],
        dims["player"]["width"]
    )
    subwindow2.box()
    panel2 = curses.panel.new_panel(subwindow2)

    fill_player_window(subwindow1, max_height, max_width)
    fill_player_window(subwindow2, max_height, max_width)
    return (panel1, panel2)


def fill_player_window(window, max_height: int, max_width: int):
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
    command_window = curses.newwin(
        dims["command"]["height"],
        dims["command"]["width"],
        dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"] +
        dims["history"]["height"],
        0
    )
    command_window.box()
    panel3 = curses.panel.new_panel(command_window)

    command_window.addstr(1, 1, "Player 1 turn:")
    command_window.keypad(True)
    return (command_window, panel3)


def main_loop(command_window, history_window):
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


def main(screen):
    curses.mousemask(True)
    curses.echo()

    max_height, max_width = screen.getmaxyx()




    dims = dims_for_game(max_height, max_width)

    # Title window
    title_panel = get_title_panel(dims["title"]["height"], dims["title"]["width"], 0, 0)

    # Subtitle windows
    sub_title_panel1, sub_title_panel2 = get_subtitle_panels(dims)

    # Player windows
    panel1, panel2 = get_player_panels(dims, max_height, max_width)

    # History window
    history_window, history_panel = get_history_panel(dims)

    # Command window
    command_window, command_panel = get_command_panel(dims)

    curses.panel.update_panels()
    curses.doupdate()

    main_loop(command_window, history_window)


curses.wrapper(main)

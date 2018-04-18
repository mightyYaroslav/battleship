import time
from functools import reduce

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

screen = curses.initscr()
screen.keypad(True)

# noecho(): stops symbol echoing
# curs_set(False): prevents cursor from showing
# curses.LINES: int with scree lines


def validate_command(cmd: str) -> bool:
    return isinstance(cmd, str) and len(cmd) == 2 and ord('a') <= ord(cmd[0]) <= ord('j') and cmd[1].isnumeric()

max_height, max_width = screen.getmaxyx()

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

# Title window
title_window = curses.newwin(
    dims["title"]["height"],
    dims["title"]["width"],
    0,
    0
)
title_panel = curses.panel.new_panel(title_window)
title_window.addstr("The Battleship Game", curses.A_BOLD and curses.A_BLINK)

# Subtitle windows
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

# Player windows
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

for i in range(max_width // 4 - 5, max_width // 4 + 5):
    for j in range(max_height // 4 - 5, max_height // 4 + 5):
        subwindow1.addstr(j, i, "-")
        subwindow2.addstr(j, i, "-")

for j in range(max_height // 4 - 5, max_height // 4 + 5):
    subwindow1.addstr(j, max_width // 4 - 6, chr(65 + j - max_height // 4 + 5))
    subwindow2.addstr(j, max_width // 4 - 6, chr(65 + j - max_height // 4 + 5))

for i in range(max_width // 4 - 5, max_width // 4 + 5):
    subwindow1.addstr(max_height // 4 - 6, i, str(i - max_width // 4 + 5))
    subwindow2.addstr(max_height // 4 - 6, i, str(i - max_width // 4 + 5))

# History window
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

# Command window
command_window = curses.newwin(
    dims["command"]["height"],
    dims["command"]["width"],
    dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"] +
    dims["history"]["height"],
    0
)
command_window.box()
panel3 = curses.panel.new_panel(command_window)
curses.panel.update_panels()
curses.doupdate()

curses.panel.update_panels()
curses.doupdate()

command_window.addstr(1, 1, "Player 1 turn:")
command_window.keypad(True)
# command_window.nodelay(1)

player1_turn = True

while True:
    command_window.move(2, 1)
    key = command_window.getstr()
    if len(key) == 0:
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

curses.nocbreak()
screen.keypad(False)
curses.echo()
curses.endwin()

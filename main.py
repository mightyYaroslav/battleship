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


import curses
import curses.panel
from curses.textpad import Textbox, rectangle

window = curses.initscr()
running = True

# noecho(): stops symbol echoing
# curs_set(False): prevents cursor from showing
# keypad(window, True): turns keypad on
# curses.LINES: int with scree lines

max_height, max_width = window.getmaxyx()

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
for (k, v) in dims.items():
    for (dim_key, dim_val) in v.items():
        if dim_key == "height":
            sumheight += dim_val

dims["history"]["height"] = max_height - sumheight


# Title window
title_window = curses.newwin(dims["title"]["height"], dims["title"]["width"], 0, 0)
title_panel = curses.panel.new_panel(title_window)
title_window.addstr("The Battleship Game", curses.A_BOLD and curses.A_BLINK)

# Subtitle windows
sub_title_window1 = curses.newwin(dims["subtitle"]["height"], dims["subtitle"]["width"], dims["title"]["height"], 0)
sub_title_panel1 = curses.panel.new_panel(sub_title_window1)
sub_title_window1.addstr("P1")

sub_title_window2 = curses.newwin(dims["subtitle"]["height"], dims["subtitle"]["width"], dims["title"]["height"], dims["subtitle"]["width"])
sub_title_panel2 = curses.panel.new_panel(sub_title_window2)
sub_title_window2.addstr("P2")


#Player windows
subwindow1 = curses.newwin(dims["player"]["height"], dims["player"]["width"], dims["title"]["height"] + dims["subtitle"]["height"], 0)
subwindow1.box()
panel1 = curses.panel.new_panel(subwindow1)

subwindow2 = curses.newwin(dims["player"]["height"], dims["player"]["width"], dims["title"]["height"] + dims["subtitle"]["height"], dims["player"]["width"])
subwindow2.box()
panel2 = curses.panel.new_panel(subwindow2)

for i in range(max_width // 4 - 5, max_width // 4 + 5):
    for j in range(max_height // 4 - 5, max_height // 4 + 5):
        subwindow1.addstr(j, i, "-")
        subwindow2.addstr(j, i, "-")


#History window
history_window = curses.newwin(dims["history"]["height"], dims["history"]["width"], dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"], 0)
history_panel = curses.panel.new_panel(history_window)

history_window.addstr("History:\n")



# Command window
command_window = curses.newwin(dims["command"]["height"], dims["command"]["width"], dims["title"]["height"] + dims["subtitle"]["height"] + dims["title"]["height"] + dims["player"]["height"] + dims["history"]["height"], 0)
command_window.box()
panel3 = curses.panel.new_panel(command_window)
curses.panel.update_panels()
curses.doupdate()

curses.panel.update_panels()
curses.doupdate()
# window.refresh()

command_window.addstr(1,1,"Player 1 turn:")

while running:
    command_window.move(2, 1)
    # str = command_window.instr(10)
    key = command_window.getch()
    # ESC
    # chr(key_code: int) -> str: return char by code
    if key == 27:
        running = False
        break
    # command_window.attron(curses.A_BLINK)
    command_window.move(2, 1)
    command_window.addstr(chr(key))
    history_window.addstr(chr(key))
    curses.panel.update_panels()
    curses.doupdate()
    # other_window.addstr(0, 0, chr(key))
    # window.move(0, 0)

curses.endwin()

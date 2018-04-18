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
# window.addstr("Hello World")
# y,x
# window.move(30, 5)
# window.addstr("Hello World2")
running = True

# noecho(): stops symbol echoing
# curs_set(False): prevents cursor from showing
# keypad(window, True): turns keypad on
# curses.LINES: int with scree lines

max_height, max_width = window.getmaxyx()

subwindow1 = curses.newwin(max_height // 2, max_width // 2, 0, 0)
subwindow1.box()
panel1 = curses.panel.new_panel(subwindow1)


subwindow2 = curses.newwin(max_height // 2, max_width // 2, 0, max_width // 2)
subwindow2.box()
panel2 = curses.panel.new_panel(subwindow2)


command_window = curses.newwin(3, max_width, max_height - 3, 0)
command_window.box()
panel3 = curses.panel.new_panel(command_window)

history_window = curses.newwin(max_height // 2 - 3, max_width, max_height // 2, 0)
history_panel = curses.panel.new_panel(history_window)

history_window.addstr("History:\n")

for i in range(max_width // 4 - 5, max_width // 4 + 5):
    for j in range( max_height // 4 - 5,  max_height // 4 + 5):
        subwindow1.addstr(j, i, "-")
        subwindow2.addstr(j, i, "-")

curses.panel.update_panels()
curses.doupdate()
# window.refresh()


while running:
    key = command_window.getch()
    # ESC
    # chr(key_code: int) -> str: return char by code
    if key == 27:
        running = False
        break
    # command_window.attron(curses.A_BLINK)
    command_window.move(1,1)
    command_window.addstr(chr(key))
    # other_window.addstr(0, 0, chr(key))
    # window.move(0, 0)

curses.endwin()

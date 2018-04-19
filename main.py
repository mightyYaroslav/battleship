import time
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
# идея: использовать стейт для точки, стейт для корабля, обсервер для наблюдения за изменениями , декоратор для
# создания точки со стейтом, класс игры как синглтон
# для сохранения данных использовать историю, а ввод комманд обрабатывать шаблоном "комманда"
# Видимость полей контролируется с помощью прокси


import curses
import curses.panel
import signal


def validate_command(cmd: str) -> bool:
    return isinstance(cmd, str) and len(cmd) == 2 and ord('a') <= ord(cmd[0].lower()) <= ord('j') and cmd[1].isnumeric()


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
    return title_window, title_panel


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
    return subtitle1_panel, subtitle2_panel


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
    return p1_window, p1_panel, p2_window, p2_panel


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


def game_loop(dims, command_window, history_window, player1_window, player2_window, p1_field, p2_field, max_width,
              max_height):
    player1_turn = True
    while True:
        command_window.move(2, 1)
        binput = command_window.getstr()
        if len(binput) == 0:
            break
        if not validate_command(binput.decode("utf-8")):
            command_window.move(2, 1)
            command_window.addstr("Input is incorrect!")
            command_window.refresh()
            time.sleep(1)
            command_window.move(2, 1)
            command_window.clrtoeol()
            continue
        command_window.move(2, 1)
        history_window.addstr(("P1: " if player1_turn else "P2: ") + binput.decode("utf-8") + "\n")
        if player1_turn:
            player_window = player1_window
            enemy_window = player2_window
            player_field = p1_field
            enemy_field = p2_field
        else:
            player_window = player2_window
            enemy_window = player1_window
            player_field = p2_field
            enemy_field = p1_field

        # player_field.put_ships(player_window)
        # player_field.add_coordinates(player_window, max_width, max_height)
        # player_window.refresh()
        #
        # enemy_field.put_empty(enemy_window, max_width, max_height)
        # enemy_field.add_coordinates(enemy_window, max_width, max_height)
        # enemy_window.refresh()

        command = binput.decode("utf-8")
        strike_y = ord(command[0].lower()) - ord('a') + dims["player"]["height"] // 2 - 5
        strike_x = int(command[1]) + dims["player"]["width"] // 2 - 5
        # TODO Check Field coords!
        gotcha = enemy_field.launch(strike_x, strike_y)

        enemy_window.addstr(strike_y, strike_x, "K" if gotcha else "M")

        curses.panel.update_panels()
        curses.doupdate()
        player1_turn = not player1_turn
        command_window.clrtoeol()
        command_window.addstr(1, 1, "Player " + ("1" if player1_turn else "2") + " turn:")


def belongs_to_player(player_num: int, x: int, y: int) -> bool:
    if player_num == 1:
        pass
    return True


def setup_loop(screen, max_y, max_x, min_y, min_x):
    ship_size = 1
    i = 0
    f = Field(10, 10)
    ship_pts = []
    vert = True
    while True:

        if len(ship_pts) == ship_size:
            xs = [pt.x for pt in ship_pts]
            ys = [pt.y for pt in ship_pts]
            f.add_ship(Ship(Point(min(xs), min(ys)), Point(max(xs), max(ys))))
            ship_pts = []
            i += 1
            if i == 5:
                break
            elif i == 5 + 1 - ship_size:
                ship_size -= 1
                i = 0

        e = screen.getch()
        if e == ord('q'):
            break

        if e == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            if min_x <= mx <= max_x and min_y <= my <= max_y:
                if len(ship_pts) == 0:
                    screen.addstr(my, mx, "x")
                    ship_pts.append(Point(int(mx), int(my)))

                for pt in ship_pts:
                    if len(ship_pts) == 1 and (
                            (abs(pt.x - mx) == 1 and pt.y == my) or (abs(pt.y - my) == 1 and pt.x == mx)):
                        vert = (abs(pt.x - mx) == 1 and pt.y == my)
                        screen.addstr(my, mx, "x")
                        ship_pts.append(Point(int(mx), int(my)))
                        break

                    elif (vert and (abs(pt.x - mx) == 1 and pt.y == my)) or \
                            (not vert and (abs(pt.y - my) == 1 and pt.x == mx)):
                        screen.addstr(my, mx, "x")
                        ship_pts.append(Point(int(mx), int(my)))
                        break

    return f


def check_ship(length: int) -> bool:
    return False


def main(screen):
    max_height, max_width = screen.getmaxyx()

    dims = dims_for_game(max_height, max_width)

    # Setup

    # Title window
    title_window, title_panel = get_title_panel(dims)

    # Subtitle windows
    subtitle1_panel, subtitle2_panel = get_subtitle_panels(dims)

    # Player windows
    player1_window, player1_panel, player2_window, player2_panel = get_player_panels(dims, max_height, max_width)

    curses.mousemask(True)
    curses.curs_set(False)
    curses.noecho()

    curses.panel.update_panels()
    curses.doupdate()

    p1_field = setup_loop(
        screen,
        dims["player"]["height"] // 2 + 6,
        dims["player"]["width"] // 2 + 4,
        dims["player"]["height"] // 2 - 3,
        dims["player"]["width"] // 2 - 5
    )

    # player1_window.clear()
    # player1_window.refresh()
    p1_field.put_empty(player1_window, max_width, max_height)
    p1_field.add_coordinates(player1_window, max_width, max_height)
    player1_window.refresh()

    p2_field = setup_loop(
        screen,
        dims["player"]["height"] // 2 + 6,
        dims["player"]["width"] // 2 * 3 + 5,
        dims["player"]["height"] // 2 - 3,
        dims["player"]["width"] // 2 * 3 - 4
    )

    p2_field.put_empty(player2_window, max_width, max_height)
    p2_field.add_coordinates(player2_window, max_width, max_height)
    player2_window.refresh()

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

    game_loop(dims, cmd_window, history_window, player1_window, player2_window, p1_field, p2_field, max_width,
              max_height)


try:
    curses.wrapper(main)
except KeyboardInterrupt as e:
    print("Exit")

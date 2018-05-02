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
# Можно использовать декоратор для добавления поля убил/попал в саму точку


import curses
import curses.panel
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

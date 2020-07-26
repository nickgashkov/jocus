import curses
import random
from dataclasses import dataclass
from typing import NamedTuple, Set, Union

from jocus import voice


def enqueue() -> None:
    curses.wrapper(render)


class Screen(NamedTuple):
    x: int
    y: int


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def update(self, key: Union[int, str]) -> None:
        if key == "KEY_UP":
            self.x -= 1
        elif key == "KEY_DOWN":
            self.x += 1
        elif key == "KEY_LEFT":
            self.y -= 1
        elif key == "KEY_RIGHT":
            self.y += 1

    def normalize(self, screen: Screen) -> None:
        self.x = self.x % screen.x
        self.y = self.y % screen.y


class Coin(NamedTuple):
    x: int
    y: int

    @classmethod
    def spawn(cls, screen: Screen) -> "Coin":
        return Coin(x=random.randint(0, screen.x), y=random.randint(0, screen.y),)


def render(window: curses.window) -> None:
    curses.curs_set(0)

    screen = Screen(*window.getmaxyx())
    position = Position()
    coins = {Coin.spawn(screen) for __ in range(5)}

    while True:
        render_once(window, screen, position, coins)


def render_once(
    window: curses.window, screen: Screen, position: Position, coins: Set[Coin]
) -> None:
    position.update(window.getkey())
    position.normalize(screen)

    window.clear()

    for coin in coins:
        window.addstr(coin.x, coin.y, "o")

    window.addstr(position.x, position.y, "*")

    if Coin(x=position.x, y=position.y) in coins:
        coins.discard(Coin(x=position.x, y=position.y))
        voice.say("о")

        if not coins:
            voice.say("молодец")

    window.refresh()

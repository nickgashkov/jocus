from __future__ import annotations

import curses
import dataclasses
import random
from typing import NamedTuple, Set, Union

from jocus import voice


class Bounds(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class Player:
    bounds: Bounds
    x: int = 0
    y: int = 0

    def move(self, key: Union[int, str]) -> None:
        if key == "KEY_UP":
            self.x -= 1
        elif key == "KEY_DOWN":
            self.x += 1
        elif key == "KEY_LEFT":
            self.y -= 1
        elif key == "KEY_RIGHT":
            self.y += 1

        self.x = self.x % self.bounds.x
        self.y = self.y % self.bounds.y

    def maybe_grab_coin(self, coins: Set[Coin]) -> None:
        coin = Coin(self.x, self.y)
        coin.grab(coins)


class Coin(NamedTuple):
    x: int
    y: int

    @classmethod
    def spawn(cls, bounds: Bounds) -> Coin:
        return Coin(
            x=random.randint(0, bounds.x - 1), y=random.randint(0, bounds.y - 1)
        )

    def grab(self, container: Set[Coin]) -> None:
        if self in container:
            container.discard(self)
            voice.say("о")


@dataclasses.dataclass
class State:
    bounds: Bounds
    player: Player
    coins: Set[Coin]

    is_finished: bool = False

    @classmethod
    def collect(cls, window: curses.window) -> State:
        bounds = Bounds(*window.getmaxyx())
        player = Player(bounds=bounds)
        coins = {Coin.spawn(bounds) for __ in range(5)}

        return State(bounds=bounds, player=player, coins=coins)

    def update(self, window: curses.window) -> None:
        self.player.move(window.getkey())
        self.player.maybe_grab_coin(self.coins)

        if not self.coins and not self.is_finished:
            self.is_finished = True
            voice.say("молодец")

    def render(self, window: curses.window) -> None:
        window.clear()

        for coin in self.coins:
            window.addstr(coin.x, coin.y, "o")

        window.addstr(self.player.x, self.player.y, "*")

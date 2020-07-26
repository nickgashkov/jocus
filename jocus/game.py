import curses

from jocus.state import State


def enqueue() -> None:
    curses.wrapper(render)


def render(window: curses.window) -> None:
    curses.curs_set(0)

    render_welcome_screen(window)
    render_game(window)


def render_welcome_screen(window: curses.window) -> None:
    window.clear()

    window.addstr(0, 10, "jocus 0.0.1")
    window.addstr(1, 10, "collect coins and you win")
    window.addstr(3, 10, "press any key to start...")

    window.refresh()


def render_game(window: curses.window) -> None:
    state = State.collect(window)

    while True:
        render_game_frame(window, state)


def render_game_frame(window: curses.window, state: State) -> None:
    state.update(window)
    state.render(window)

    window.refresh()

import curses
from screens.login_screen import on_load_login_screen
from screens.home_screen import on_load_home_screen
from screens.game_screen import on_load_game_screen
from screens.champions_screen import on_load_champions_screen
from screens.outcome_screen import on_load_outcome_screen
from config import consts
from config import palette

def main():
    palette.init_colors()
    on_load_login_screen(curses.wrapper)

    screen = consts.HOME_SCREEN
    while True:
        if screen == consts.HOME_SCREEN:
            screen = on_load_home_screen(curses.wrapper)
        elif screen == consts.GAME_SCREEN:
            screen = on_load_game_screen(curses.wrapper)
        elif screen == consts.CHAMPIONS_SCREEN:
            screen = on_load_champions_screen(curses.wrapper)
        elif screen == consts.OUTCOME_SCREEN:
            screen = on_load_outcome_screen(curses.wrapper)
        else:
            return

main()

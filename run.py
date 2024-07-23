import curses
from screens.home_screen import on_load_home_screen
from screens.main_menu_screen import on_load_main_menu_screen
from config import consts
from config import palette


def main():
    palette.init_colors()
    screen = consts.HOME_SCREEN
    while True:
        if screen == consts.HOME_SCREEN:
            screen = on_load_home_screen(curses.wrapper)
        elif screen == consts.MAIN_MENU_SCREEN:
            screen = on_load_main_menu_screen(curses.wrapper)
        else:
            return

main()

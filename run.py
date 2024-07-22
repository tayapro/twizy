import curses
from screens.home_screen import on_load_home_screen
from screens.main_menu_screen import on_load_main_menu_screen
from consts import screens

def main():
    screen = screens.HOME_SCREEN
    while True:
        if screen == screens.HOME_SCREEN:
            screen = on_load_home_screen(curses.wrapper)
        elif screen == screens.MAIN_MENU_SCREEN:
            screen = on_load_main_menu_screen(curses.wrapper)
        else:
            return

main()

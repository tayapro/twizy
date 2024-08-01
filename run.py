import curses
import logging
from screens.login_screen import on_load_login_screen
from screens.home_screen import on_load_home_screen
from screens.game_screen import on_load_game_screen
from screens.champions_screen import on_load_champions_screen
from screens.outcome_screen import on_load_outcome_screen
from screens.error_screen import on_load_error_screen
from config import screens, palette
from lib.spreadsheet_storage import init_storage


logging.basicConfig(
    filename="twizy.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)


def main():
    screen = screens.HOME_SCREEN

    init_storage()
    palette.init_colors()

    while True:
        try:
            on_load_login_screen(curses.wrapper)
            break
        except Exception as e:
            logging.error(f"what is going on here {e}")
            s = on_load_error_screen(curses.wrapper)
            if s == None:
                return

    while True:
        try:
            if screen == screens.HOME_SCREEN:
                screen = on_load_home_screen(curses.wrapper)
            elif screen == screens.GAME_SCREEN:
                screen = on_load_game_screen(curses.wrapper)
            elif screen == screens.CHAMPIONS_SCREEN:
                screen = on_load_champions_screen(curses.wrapper)
            elif screen == screens.OUTCOME_SCREEN:
                screen = on_load_outcome_screen(curses.wrapper)
            else:
                return
            logging.info(f"SCREEN: {screen}")
        except Exception as e:
            logging.error(f"Error on {screen} screen: {e}")
            screen = on_load_error_screen(curses.wrapper)


if __name__ == "__main__":
#     pytest.main()      
    main()

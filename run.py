import curses
import logging
from screens.login_screen import on_load_login_screen
from screens.home_screen import on_load_home_screen
from screens.game_screen import on_load_game_screen
from screens.champions_screen import on_load_champions_screen
from screens.outcome_screen import on_load_outcome_screen
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

logging.debug("This is debug")
logging.info("This is info")
logging.warning("This is warning")
logging.error("This is error")


def main():
    init_storage()
    palette.init_colors()
    on_load_login_screen(curses.wrapper)

    screen = screens.HOME_SCREEN
    while True:
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


main()

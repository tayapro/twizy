import curses
import logging
from screens.login_screen import on_load_login_screen
from screens.home_screen import on_load_home_screen
from screens.game_screen import on_load_game_screen
from screens.champions_screen import on_load_champions_screen
from screens.outcome_screen import on_load_outcome_screen
from screens.error_screen import on_load_error_screen
from config import screens, palette
from lib import spreadsheet_storage


logging.basicConfig(
    filename="twizy.log",
    encoding="utf-8",
    filemode="a",
    format='%(asctime)s  %(levelname)-8s [%(filename)s:%(lineno)d]  %(message)s',
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)

def main():
    """
    The function sets up initial configurations, manages screen transitions
    based on user actions, and handles exceptions by logging errors and
    displaying an error screen if necessary.
    """
    # Set the initial screen to the home screen
    screen = screens.LOGIN_SCREEN

    # Initialize storage and palette configurations
    spreadsheet_storage.init_storage()
    palette.init_colors()

    # Main loop for handling different screens
    while True:
        try:
            # Determine which screen to load based on the current screen state
            if screen == screens.LOGIN_SCREEN:
                screen = on_load_login_screen(curses.wrapper)
            if screen == screens.HOME_SCREEN:
                screen = on_load_home_screen(curses.wrapper)
            elif screen == screens.GAME_SCREEN:
                screen = on_load_game_screen(curses.wrapper)
            elif screen == screens.CHAMPIONS_SCREEN:
                screen = on_load_champions_screen(curses.wrapper)
            elif screen == screens.OUTCOME_SCREEN:
                screen = on_load_outcome_screen(curses.wrapper)
            else:
                return  # Exit if anything else (we use None)
                
            logging.info(f"Screen transitioned to: {screen}")

        except KeyboardInterrupt:
            logging.info("The user interrupts the execution of a program")
            return
        except Exception as e:
            logging.critical(f"Error on {screen} screen: {e}")
            screen = on_load_error_screen(curses.wrapper)


if __name__ == "__main__":
    main()

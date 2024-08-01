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

# Configure logging for the application
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
    """
    The main function that initializes the game and handles screen navigation.

    This function sets up initial configurations, manages screen transitions
    based on user actions, and handles exceptions by logging errors and
    displaying an error screen if necessary.
    """
    # Set the initial screen to the home screen
    screen = screens.HOME_SCREEN

    # Initialize storage and palette configurations
    init_storage()
    palette.init_colors()

    # Load the login screen, handling any exceptions
    while True:
        try:
            on_load_login_screen(curses.wrapper)
            break  # Exit loop if successful
        except Exception as e:
            logging.error(f"Exception occurred during login screen load: {e}")
            s = on_load_error_screen(curses.wrapper)
            if s is None:
                return  # Exit if the error screen returns None

    # Main loop for handling different screens
    while True:
        try:
            # Determine which screen to load based on the current screen state
            if screen == screens.HOME_SCREEN:
                screen = on_load_home_screen(curses.wrapper)
            elif screen == screens.GAME_SCREEN:
                screen = on_load_game_screen(curses.wrapper)
            elif screen == screens.CHAMPIONS_SCREEN:
                screen = on_load_champions_screen(curses.wrapper)
            elif screen == screens.OUTCOME_SCREEN:
                screen = on_load_outcome_screen(curses.wrapper)
            else:
                return  # Exit if an invalid screen state is encountered
            logging.info(f"Screen transitioned to: {screen}")
        except Exception as e:
            logging.error(f"Error on {screen} screen: {e}")
            screen = on_load_error_screen(curses.wrapper)


if __name__ == "__main__":
    main()

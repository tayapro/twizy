import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    BLUE_AND_CYAN = curses.color_pair(1)
    YELLOW_AND_BLACK = curses.color_pair(2)

    warning_window = curses.newwin(1, 30, 15, 10)

    game_name = "tWIZY"
    key = None

    while True:
        # Clear screen
        stdscr.clear()
        # Clear warning window
        warning_window.clear()

        stdscr.addstr(4, 30, "                                       ", BLUE_AND_CYAN)
        stdscr.addstr(5, 30, "                   ", BLUE_AND_CYAN)
        stdscr.addstr(5, 46, game_name, BLUE_AND_CYAN | curses.A_BOLD)
        stdscr.addstr(5, 46 + len(game_name), "                  ", BLUE_AND_CYAN)
        stdscr.addstr(6, 30, "                                       ", BLUE_AND_CYAN)
        stdscr.addstr(8, 30, "<-====== wizy for real hackers ======->", curses.color_pair(2) | curses.A_ITALIC)

        """
        Welcome page
        """
        # Instructions for the user
        input_name = "Enter your name: "
        stdscr.addstr(10, 30, input_name)
        stdscr.refresh()
        if input_name != '' and key == curses.KEY_ENTER:
            curses.setsyx(11, 51)

        input_password = "Enter your password: "
        stdscr.addstr(11, 30, input_password)
        if input_password == '' and key == curses.KEY_ENTER:
            warning_window.addnstr("You need to provide a password")
            
            
        stdscr.refresh()

        # Create an input window for name
        # nlines - 1, ncolumns - 12 (login's length), 
        # begin_y - 10, begin_x - 30 (begin_x for instructions) +  len(instructions)
        input_window_name = curses.newwin(1, 12, 10, 30 + len(input_name))
        input_window_password = curses.newwin(1, 12, 11, 30 + len(input_password))
        curses.echo()  # Enable echoing of input characters

        # Get user input name
        user_input_name = input_window_name.getstr().decode('utf-8')
        user_input_password = input_window_password.getstr().decode('utf-8')

        """
        Menu page
        """
        # Clear screen and display the entered input
        stdscr.clear()
        stdscr.addstr(0, 0, f"Hello, {user_input_name}!")
        stdscr.addstr(1, 0, f"Your password is {user_input_password}!")
        stdscr.refresh()

        # Wait for user input before exiting
        character = stdscr.getch()
        if character == ord('q'):
            break

wrapper(main)

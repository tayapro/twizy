import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    BLUE_AND_CYAN = curses.color_pair(1)
    YELLOW_AND_BLACK = curses.color_pair(2)

    # Clear screen
    stdscr.clear()

    stdscr.addstr(5, 30, "  tWizy  ", BLUE_AND_CYAN | curses.A_BOLD)
    stdscr.addstr(5, 46, "  tWizy  ", BLUE_AND_CYAN | curses.A_BOLD)
    stdscr.addstr(6, 30, "<-====== wizy for real hackers ======->", curses.color_pair(2) | curses.A_ITALIC)

    # Instructions for the user
    instructions = "Enter your name: "
    stdscr.addstr(10, 30, instructions)
    stdscr.refresh()

    # Create an input window
    # nlines - 1, ncolumns - 12 (login's length), 
    # begin_y - 10, begin_x - 30 (begin_x for instructions) +  len(instructions)
    input_window = curses.newwin(1, 12, 10, 30 + len(instructions))
    curses.echo()  # Enable echoing of input characters

    # Get user input
    user_input = input_window.getstr().decode('utf-8')

    # Clear screen and display the entered input
    stdscr.clear()
    stdscr.addstr(0, 0, f"Hello, {user_input}!")
    stdscr.refresh()


    # Wait for user input before exiting
    stdscr.getch()

wrapper(main)

import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Instructions for the user
    instructions = "Enter your name: "
    stdscr.addstr(0, 0, instructions)
    stdscr.refresh()

    # Create an input window
    input_window = curses.newwin(1, 40, 1, len(instructions))
    curses.echo()  # Enable echoing of input characters

    # Get user input
    user_input = input_window.getstr().decode('utf-8')

    # Clear screen and display the entered input
    stdscr.clear()
    stdscr.addstr(0, 0, f"Hello, {user_input}!")
    stdscr.refresh()

    # Wait for user input before exiting
    stdscr.getch()

curses.wrapper(main)

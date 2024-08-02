import curses

# Define box-drawing characters for curses
setattr(curses, "ACS_VLINE", "|")
setattr(curses, "ACS_HLINE", "-")
setattr(curses, "ACS_ULCORNER", "+")
setattr(curses, "ACS_URCORNER", "+")
setattr(curses, "ACS_LRCORNER", "+")
setattr(curses, "ACS_LLCORNER", "+")
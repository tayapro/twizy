import sys
import os

# Ensure the correct path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import curses

# Define box-drawing characters for curses
setattr(curses, "ACS_VLINE", "|")
setattr(curses, "ACS_HLINE", "-")
setattr(curses, "ACS_ULCORNER", "+")
setattr(curses, "ACS_URCORNER", "+")
setattr(curses, "ACS_LRCORNER", "+")
setattr(curses, "ACS_LLCORNER", "+")
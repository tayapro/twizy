import curses

def demo(screen):
    # save the colors and restore it later
    save_colors = [curses.color_content(i) for i in range(curses.COLORS)]
    curses.curs_set(0)
    curses.start_color()

    # use 250 to not interfere with tests later
    curses.init_color(250, 1000, 0, 0)
    curses.init_pair(250, 250, curses.COLOR_BLACK)
    curses.init_color(251, 0, 1000, 0)
    curses.init_pair(251, 251, curses.COLOR_BLACK)

    screen.addstr(0, 20, 'Test colors for r,g,b = {0, 200}\n',
                  curses.color_pair(250) | curses.A_BOLD | curses.A_UNDERLINE)
    i = 0
    for r in (0, 200):
        for g in (0, 200):
            for b in (0, 200):
                i += 1
                curses.init_color(i, r, g, b)
                curses.init_pair(i, i, curses.COLOR_BLACK)
                screen.addstr('{},{},{}  '.format(r, g, b), curses.color_pair(i))

    screen.addstr(3, 20, 'Test colors for r,g,b = {0..1000}\n',
                  curses.color_pair(251) | curses.A_BOLD | curses.A_UNDERLINE)
    for r in range(0, 1001, 200):
        for g in range(0, 1001, 200):
            for b in range(0, 1001, 200):
                i += 1
                curses.init_color(i, r, g, b)
                curses.init_pair(i, i, curses.COLOR_BLACK)
                screen.addstr(' ({},{},{}) '.format(r, g, b), curses.color_pair(i))
                screen.addstr('test |', curses.color_pair(i))

    screen.getch()
    # restore colors
    for i in range(curses.COLORS):
        curses.init_color(i, *save_colors[i])
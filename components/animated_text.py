import time

class AnimatedText(object):
    def __init__(self, message, y, x, delay, *args):
        self._message = message
        self.y = y
        self.x = x
        self.delay = delay
        self.args = args[:]
        self.displayed_message = ""

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self.displayed_message = ""

    # def restart(self):
    #     self.displayed_message = ""

    def draw(self, stdscr):
        if not self.is_animation_finished():
            self.displayed_message += self._message[len(self.displayed_message)]
            time.sleep(self.delay)
        stdscr.addstr(self.y, self.x, self.displayed_message, *self.args)

    def is_animation_finished(self):
        return len(self.displayed_message) == len(self._message)
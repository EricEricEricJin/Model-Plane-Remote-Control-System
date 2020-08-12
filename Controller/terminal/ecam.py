"""
    Use curses
"""

import curses

class Ecam:
    

    def __init__(self):
        self.error_list = []
        self._init_window()

    def _init_window(self):
        self.main_win = curses.initscr()
        curses.noecho()

        self.main_win.addch("a")
        self.err_win = self.main_win.subwin(0, 0)
        self.main_win.getch()
        curses.endwin()


    def _home_page(self, key_val):
        self.main_win.getch()

    def _checklist(self):
        pass


E = Ecam()
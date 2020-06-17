from tkinter import *
from md import MD
from pdb import set_trace


class mainWin:
    def __init__(self, WIN_H, WIN_W):

        self.WIN_H = WIN_H
        self.WIN_W = WIN_W
        self.window = Tk()
        self.window.geometry(str(WIN_W) + "x" + str(WIN_H))

        self.menu_bar = Menu(self.window)

        self.all_frames = []
        for frame in [MD]:
            f = frame(self.window, self.WIN_H, self.WIN_W)
            self.all_frames.append(f.frame)
        set_trace()

        for menu_cmd in ["MD"]:
            self.menu_bar.add_command(label = menu_cmd, command = lambda:self._change_to(menu_cmd))


        self.window.config(menu = self.menu_bar)

    def run(self):
        self.window.mainloop()

    def _change_to(self, frame_name):
        print("CHANGE TO", frame_name)
        if frame_name == "MD":
            self.all_frames[0].pack()

if __name__ == "__main__":
    MW = mainWin(400,640)
    MW.run()

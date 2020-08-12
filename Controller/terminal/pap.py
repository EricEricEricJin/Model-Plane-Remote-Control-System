"""
    send tar_spd, tar_hdg, tar_hdg, tar_vs, fd_on, ap_spd, ap_hdg, ap_alt
"""

from tkinter import *

class PAP:

    WIN_H = 640
    WIN_W = 400

    def __init__(self):
        self.root = Tk()
        self.root.geometry(str(self.WIN_W) + "x" + str(self.WIN_H))
        # self.root.configure(bg = "black")

        self._init_interface()

    def _init_interface(self):
        self.txt_fd = Label(self.root, text = "FD", height = 1, width = 4, bg = "black", fg = "white")
        self.txt_fd.place(x = self.WIN_W / 16, y = 3 / 20 * self.WIN_H)

        self.bt_fd_on = Button(self.root, text = "ON", command = self._bt_fd_on_clicked, bg = "white", fg = "blue")
        self.bt_fd_on.place(x = self.WIN_W / 4, y = 3 / 20 * self.WIN_H)

        self.bt_fd_off = Button(self.root, command = self._bt_fd_off_clicked)

        self.bt_fac_on = Button(self.root, command = self._bt_fac_on_clicked)

        self.bt_fac_off = Button(self.root, command = self._bt_fac_off_clicked)

    def run(self):
        self.root.mainloop()

    def _bt_fd_on_clicked(self):
        pass

    def _bt_fd_off_clicked(self):
        pass

    def _bt_fac_on_clicked(self):
        pass

    def _bt_fac_off_clicked(self):
        pass


if __name__ == "__main__":
    P = PAP()
    P.run()


from tkinter import *

class EMD:
    pass

class engineCanvas:
    def __init__(self, master, cvs_H, cvs_W):
        self.CVS_H = cvs_H
        self.CVS_W = cvs_W

        self.cvs = Canvas(master = master, height = cvs_H, width = cvs_W, bg = "black", highlightthickness = 0)

        self.thr_ind_radians = min(1 / 3 * self.CVS_H, 2 / 5 * self.CVS_W)
        self.thr_ind_o = ()



'''
    Each terminal communicate with server by UDP
    Receive all data & send operations

    can shift windows without communicate with servo
'''

from tkinter import *

FRAME_H = 1080
FRAME_W = 1920

class MD:
    # mechanism display
    def __init__(self, master, height, width):
        self.bar_width = 10
        self.bar_height = int(height / 3)
        self.pointers = []
        self.zeros = []

        self.frame = Frame(master = master, width = width, height = height, bg = "black")
        self.canvas = Canvas(master = self.frame, width = width, height = height, bg = "black", bd = 0, highlightthickness = 0)

        texts = ["L FLA", "L AIL", "R AIL", "R FLA"]

        for i in range(4):
            self.canvas.create_rectangle(((1 + i) / 5 * width - 1 / 2 * self.bar_width), (1 / 3 * self.bar_height), ((1 + i) / 5 * width - 1 / 2 * self.bar_width + self.bar_width), (4 / 3 * self.bar_height), outline = "white",  width = 2)
            self.canvas.create_text(((1 + i) / 5 * width), (4 / 3 * self.bar_height + 10), text = texts[i], fill = "white")
            # print(((1 + i) / 5 * width - 1 / 2 * self.bar_width), ((1 + i) / 5 * width - 1 / 2 * self.bar_width + self.bar_width))

        self.canvas.create_rectangle((1 / 5 * width - 1 / 2 * self.bar_width), (5 / 3 * self.bar_height), (1 / 5 * width - 1 / 2 * self.bar_width + self.bar_width), (8 / 3 * self.bar_height), outline = "white",  width = 2)
        self.canvas.create_text((1 / 5 * width), (5 / 3 * self.bar_height + self.bar_height) + 10, text = "L ELE", fill = "white")
        self.canvas.create_rectangle((4 / 5 * width - 1 / 2 * self.bar_width), (5 / 3 * self.bar_height), (4 / 5 * width - 1 / 2 * self.bar_width + self.bar_width), (8 / 3 * self.bar_height), outline = "white",  width = 2)
        self.canvas.create_text((4 / 5 * width), (5 / 3 * self.bar_height + self.bar_height) + 10, text = "R ELE", fill = "white")

        self.canvas.create_rectangle((2 / 5 * width - 1 / 2 * self.bar_width - int(width / 20)), (8 / 3 * self.bar_height) - self.bar_width, (3 / 5 * width + 1 / 2 * self.bar_width + int(width / 20)), (8 / 3 * self.bar_height), outline = "white", width = 2)
        self.canvas.create_text(int(width / 2), (8 / 3 * self.bar_height) + 10, text = "RUD", fill = "white")

        self.canvas.pack()
        # self.frame.pack()
        # return self.frame

    def change_to(self, flap_l, aile_l, aile_r, flap_r, ele_l, rud, ele_r):
        self.canvas.create_polygon()


if __name__ == "__main__":
    root = Tk("MD")
    root.geometry("640x800")
    root.configure(bg = "black")
    M = MD(root, 800, 640)
    root.mainloop()

from math import sin, cos, pi

from threading import Thread
from time import sleep
from tkinter import *
from PIL import Image, ImageTk

class Engine:
    def __init__(self, master, length, place_x, place_y):
        self.length = length
        self.frame = Frame(master = master, width = length, height = length, bg = "black")
        
        self.arc = Canvas(self.frame, width = length, height = length, bg = "black", bd = 0, highlightthickness = 0)
        self.arc.create_arc(5, 5, length - 5, length - 5, start = 0, extent = 225, style = ARC, outline = "white", width = 2)
        self.arc.create_rectangle(0.5 * length, 0.6 * length, 0.9 * length, 0.9 * length, outline = "white", width = 2)
        self.arc.pack()
        # self.frame.pack(side = pack_side, fill = "both")
        self.frame.place(x = place_x, y = place_y)
        self.r = length / 2 - 5
        self.center = (int(length / 2), int(length / 2))


    def turn_on(self, val_min, val_max):
        self.val = 0
        self.val_max = val_max
        self.val_min = val_min
        self.text_color = "green"
        self.arc.create_text(0.25 * self.length, 0.8 * self.length, text = str(val_min), fill = "white", font=("Menlo", int(self.length / 15)))
        self.arc.create_text(0.9 * self.length, 0.55 * self.length, text = str(val_max), fill = "white", font=("Menlo", int(self.length / 15)))
        # self.text = self.arc.create_text(0.75 * self.length, 0.8 * self.length, text = str(self.val), fill = self.text_color)
        self.text = self.arc.create_text(0.7 * self.length, 0.75 * self.length, text = "", fill = self.text_color, font = ("Menlo", int(self.length / 15)))
        self.pointer = self.arc.create_line(self.center, (self._val2pos(0)[0] + self.center[0], self.length - (self._val2pos(0)[1] + self.center[1])), fill = "green", width = 3)
        self.arc.pack()

    def change_to(self, val):

        self.val = val
        self.arc.coords(self.pointer, self.center[0], self.center[1], self._val2pos(val)[0] + self.center[0], self.length - (self._val2pos(val)[1] + self.center[1]))
        self.arc.itemconfig(self.text, text = str(val))
        self.arc.pack()

    def _val2pos(self, val):
        return (
            int(cos((self.val_max - val) / (self.val_max - self.val_min) * (5/4) * pi) * self.r),
            int(sin((self.val_max - val) / (self.val_max - self.val_min) * (5/4) * pi) * self.r)
        )

class rollBar:
    
    def __init__(self, master, width, height, LoR, place_x, place_y):
        self.LoR = LoR
        self.frame = Frame(master = master, width = width, height = height, bg = "black")
        self.frame.place(x = place_x, y = place_y)
        self.canvas = Canvas(self.frame, width = width, height = height, bg = "grey", bd = 0, highlightthickness = 0)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.div_len = height / 4
        self.lines = []
        self.numbers = []
        if LoR == "L":
            self.canvas.create_rectangle(10, int(self.height / 2) + 6, self.width - 1, int(self.height / 2) - 6, outline = "white", fill = "black")
        elif LoR == "R":
            self.canvas.create_rectangle(0, int(self.height / 2) + 6, self.width - 11, int(self.height / 2) - 6, outline = "white", fill = "black")

    def turn_on(self, div):
        self.div = div
        if self.LoR == "L":
            self.canvas.create_polygon(10, int(self.height / 2) + 6, 10, int(self.height / 2) - 6, 0, int(self.height / 2), fill = "white")
        elif self.LoR == "R":
            self.canvas.create_polygon(self.width - 11, int(self.height / 2) + 6, self.width - 11, int(self.height / 2) - 6, self.width - 1, int(self.height / 2), fill = "white")
        self.change_to(0)
        

    def change_to(self, val):
        # del lines and numbers
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        for number in self.numbers:
            self.canvas.delete(number)
        self.lines = []

        # draw lines and numbers
        delta_h = (val % self.div) * (self.div_len / self.div)
        y = int(self.height / 2 + delta_h)
        y_val = val - (val % self.div)

        delta_y = 0
        delta_y_val = 0

        if self.LoR == "L":
            while delta_y + y < self.height:
                self.lines.append(self.canvas.create_line((0, y + delta_y), (int(self.width / 2), y + delta_y), fill = "white", width = 2))
                self.numbers.append(self.canvas.create_text(self.width * 0.75, y + delta_y, text = str(y_val - delta_y_val), fill = "white", font=("Menlo", int(self.width / 5))))
                dd_y = 0
                while delta_y + y + dd_y < self.height and dd_y < self.div_len:
                    self.lines.append(self.canvas.create_line((0, y + delta_y + dd_y), (int(self.width / 4), y + delta_y + dd_y), fill = "white", width = 1))
                    dd_y += int(self.div_len / 5)
                delta_y += self.div_len
                delta_y_val += self.div

            delta_y = 0
            # delta_y = self.div_len
            delta_y_val = 0
            # delta_y_val = self.div

            while y - delta_y >= 0:
                self.lines.append(self.canvas.create_line((0, y - delta_y), (int(self.width / 2), y - delta_y), fill = "white", width = 2))
                self.numbers.append(self.canvas.create_text(int(self.width * 0.75), y - delta_y, text = str(y_val + delta_y_val), fill = "white", font=("Menlo", int(self.width / 5))))
                dd_y = 0
                while y - delta_y - dd_y >= 0 and dd_y < self.div_len:
                    self.lines.append(self.canvas.create_line((0, y - delta_y - dd_y), (int(self.width / 4), y - delta_y - dd_y), fill = "white", width = 1))
                    dd_y += int(self.div_len / 5)
                delta_y += self.div_len
                delta_y_val += self.div
            
            self.canvas.create_rectangle(10, int(self.height / 2) + 6, self.width - 1, int(self.height / 2) - 6, outline = "white", fill = "black")
            self.canvas.create_text(int((self.width - 10) / 2) + 10, int(self.height / 2), text = str(val), fill = "white", font=("Menlo", int(self.width / 5 + 1)))
            self.canvas.pack()

        elif self.LoR == "R":

            while delta_y + y < self.height:
                self.lines.append(self.canvas.create_line((self.width - 1, y + delta_y), (int(self.width / 2), y + delta_y), fill = "white", width = 2))
                self.numbers.append(self.canvas.create_text(self.width * 0.25, y + delta_y, text = str(y_val - delta_y_val), fill = "white", font=("Menlo", int(self.width / 5))))
                dd_y = 0
                while delta_y + y + dd_y < self.height and dd_y < self.div_len:
                    self.lines.append(self.canvas.create_line((self.width - 1, y + delta_y + dd_y), (int(self.width / 4 * 3), y + delta_y + dd_y), fill = "white", width = 1))
                    dd_y += int(self.div_len / 5)
                delta_y += self.div_len
                delta_y_val += self.div

            delta_y = 0
            # delta_y = self.div_len
            delta_y_val = 0
            # delta_y_val = self.div

            while y - delta_y >= 0:
                self.lines.append(self.canvas.create_line((self.width - 1, y - delta_y), (int(self.width / 2), y - delta_y), fill = "white", width = 2))
                self.numbers.append(self.canvas.create_text(int(self.width * 0.25), y - delta_y, text = str(y_val + delta_y_val), fill = "white", font=("Menlo", int(self.width / 5))))
                dd_y = 0
                while y - delta_y - dd_y >= 0 and dd_y < self.div_len:
                    self.lines.append(self.canvas.create_line((self.width - 1, y - delta_y - dd_y), (int(self.width / 4 * 3), y - delta_y - dd_y), fill = "white", width = 1))
                    dd_y += int(self.div_len / 5)
                delta_y += self.div_len
                delta_y_val += self.div
            
            self.canvas.create_rectangle(0, int(self.height / 2) + 6, self.width - 11, int(self.height / 2) - 6, outline = "white", fill = "black")
            self.canvas.create_text(int((self.width - 10) / 2) + 10, int(self.height / 2), text = str(val), fill = "white", font=("Menlo", int(self.width / 5 + 1)))
            self.canvas.pack()
    
class Video:
    def __init__(self, master, width, height, place_x, place_y):
        self.frame = Frame(master = master, width = width, height = height, bg = "black")
        self.frame.place(x = place_x, y = place_y)
        self.im = None

        self.canvas = Canvas(self.frame, width = width, height = height, bg = "grey", bd = 0, highlightthickness = 0)
        self.canvas.pack()


    def turn_on(self):
        pass

    def change_to(self, image):
        self.im = ImageTk.PhotoImage(image = image)
        self.canvas.create_image(0, 0, image = self.im)

class Attitude:
    def __init__(self):
        pass



class UI:
    def __init__(self):
        pass

    def init(self):
        self.main_win = Tk()
        
        self.main_win.geometry("1900x1000")
        
        V = Video(self.main_win, 960, 540, 0, 0)
        ENG_1 = Engine(self.main_win, 100, 0, 720)
        AS = rollBar(self.main_win, 20, 100, "L", 100, 720)
        
    
    def run(self):
        self.main_win.mainloop()

if __name__ == "__main__":
    U = UI()
    U.init()
    U.run()
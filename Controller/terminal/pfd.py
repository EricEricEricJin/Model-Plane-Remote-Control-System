"""
    Run on touch-scr tablet
    Recv
        pitch, roll, air-speed, gnd-speed, psr_alt, tof_alt, hdg, long, lat
        FD_ON, tar_speed, tar_alt, tar_hdg, tar_long
    and show them
    Send nothing
"""

from tkinter import *
from socket import *
from struct import unpack
from threading import Thread
import math
from com import Communicate

class PFD:
    def __init__(self):
        # self.COM = Communicate()
        # self.COM.send(b"pfd")

        self.root = Tk()
        self.root.geometry("800x1280")

        self.sta_ind_cvs = Canvas(master = self.root, height = 80, width = 800, bg = "black", highlightthickness = 0)
        self.sta_ind_cvs.place(x = 0, y = 0)
        
        self.speed_cvs = Canvas(master = self.root, height = 400, width = 160, bg = "black", highlightthickness = 0)
        self.speed_cvs.place(x = 0, y = 80)

        self.att_cvs = Canvas(master = self.root, height = 400, width = 400, bg = "black", highlightthickness = 0)
        self.att_cvs.place(x = 160, y = 80)

        self.alt_cvs = Canvas(master = self.root, height = 400, width = 160, bg = "black", highlightthickness = 0)
        self.alt_cvs.place(x = 560, y = 80)

        self.vs_cvs = Canvas(master = self.root, height = 400, width = 80, bg = "black", highlightthickness = 0)
        self.vs_cvs.place(x = 720, y = 80)

        self.hdg_cvs = Canvas(master = self.root, height = 800, width = 800, bg = "black", highlightthickness = 0)
        self.hdg_cvs.place(x = 0, y = 480)

        # init speed

        self.speed_lines = []
        self.speed_texts = []

        self.speed_cvs.create_rectangle(40, 0, 120, 400, fill = "grey")

        for i in range(8):
            self.speed_lines.append(self.speed_cvs.create_line(-114, -114, -114, -114, fill = "white"))
            self.speed_texts.append(self.speed_cvs.create_text(-114, -114, text = "0", fill = "white"))

        
        # self.speed_cvs.create_rectangle(20, 180, 140, 220, fill = "#202020")
        self.speed_cvs.create_polygon((20, 180, 80, 180, 120, 200, 80, 220, 20, 220), fill = "#202020")
        self.speed_val_text = self.speed_cvs.create_text(60, 200, text = "", fill = "white")

        # init att

        self.blue_poly = self.att_cvs.create_rectangle((0, 0, 400, 400), fill = "blue")
        self.brown_poly = self.att_cvs.create_polygon((-114, -114, -114, -114), fill = "red")

        self.att_lines = []
        self.att_texts = []

        for i in range(25):
            self.att_lines.append(self.att_cvs.create_line(-114, -114, -114, -114, fill = "white"))

        for i in range(13):
            self.att_texts.append(self.att_cvs.create_text(-114, -114, text = str(abs(60 - 10 * i)) ))
            self.att_texts.append(self.att_cvs.create_text(-114, -114, text = str(abs(60 - 10 * i)) ))




    def run(self):
        t = Thread(target = self._service)
        t.start()

        self.root.mainloop()

    def _service(self):
        while True:
            # raw = self.COM.recv()
            # speed, pitch, roll, alt, vs, hdg, lat, lon, tar_lat, tar_lon, tar_dir = unpack("", raw)
            speed, pitch, roll, alt, vs, hdg, lat, lon, tar_lat, tar_lon, tar_dir = 14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10
            # speed = int(input())
            roll = int(input("r"))
            pitch = int(input("p"))

            # update speed

            self.speed_cvs.itemconfigure(self.speed_val_text, text = str(speed))

            for i in range(8):
                self.speed_cvs.coords(self.speed_lines[i], self._rollbar_line_coord(80, 400, 50, 40, 40, 0, i - 4, 5, speed))
                self.speed_cvs.coords(self.speed_texts[i], (60, self._rollbar_line_coord(80, 400, 50, 40, 40, 0, i - 4, 5, speed)[1]))
                self.speed_cvs.itemconfigure(self.speed_texts[i], text = str(self._rollbar_num_val(speed, 5, i - 4)))

            
            # update attitude
            long_center_line_coord = self._att_line_coord(400, roll, pitch, 1839, 50, 0, 5)
            print("LCLC: ", long_center_line_coord)

            if 45 < roll <= 135:
                # left
                brown_coord = (
                    long_center_line_coord[0], long_center_line_coord[1], 
                    long_center_line_coord[2], long_center_line_coord[3],
                    0, 400,
                    0, 0
                )
                
            elif 135 < roll <= 180 or -180 < roll <= -135:
                # up
                brown_coord = (
                    long_center_line_coord[0], long_center_line_coord[1], 
                    long_center_line_coord[2], long_center_line_coord[3],
                    0, 0,
                    400, 0
                )
                pass
            elif -135 < roll <= -45:
                # right
                brown_coord = (
                    long_center_line_coord[0], long_center_line_coord[1], 
                    long_center_line_coord[2], long_center_line_coord[3],
                    400, 0,
                    400, 400
                )

                pass
            elif -45 < roll <= 45:
                # down
                brown_coord = (
                    long_center_line_coord[0], long_center_line_coord[1], 
                    long_center_line_coord[2], long_center_line_coord[3],
                    400, 400,
                    0, 400
                )

            self.att_cvs.coords(self.brown_poly, (brown_coord))

            for i in range(25):
                coord = self._att_line_coord(400, roll, pitch, 150 - (i % 2) * 50, 50, i - 12, 5)
                self.att_cvs.coords(self.att_lines[i], 
                    coord
                )
                if i % 2 == 0:
                    self.att_cvs.coords(self.att_texts[i], (coord[0] - math.cos(math.radians(roll)) * 10, coord[1] - math.sin(math.radians(roll)) * 10))
                    self.att_cvs.coords(self.att_texts[i + 1], (coord[2] + math.cos(math.radians(roll)) * 10, coord[3] + math.sin(math.radians(roll)) * 10))
            
            for i in range(26):
                self.att_cvs.itemconfigure(self.att_texts[i], angle = -roll)



    def _att_line_coord(self, a, r, p, l, d, n, u):
        """
            a: length of square
            r: roll in deg
            p: pitch in deg
            l: line length
            d: distance between lines
            n: n th line

            RETURN:
                (X0, Y0, X1, Y1)
        """

        """
            TODO: Deal with 90 deg
        """
        return (
            a / 2 - math.cos(math.radians(r)) * l / 2 - math.sin(math.radians(r)) * d * n  - math.sin(math.radians(r)) * p / u * d,
            p / u * d * math.cos(math.radians(r)) + n * math.cos(math.radians(r)) * d - math.sin(math.radians(r)) * l / 2 + 1 / 2 * a,
            a / 2 + math.cos(math.radians(r)) * l / 2 - math.sin(math.radians(r)) * d * n  - math.sin(math.radians(r)) * p / u * d,
            p / u * d * math.cos(math.radians(r)) + n * math.cos(math.radians(r)) * d + math.sin(math.radians(r)) * l / 2 + 1 / 2 * a

        )
    5
    def _rollbar_line_coord(self, w, h, d, l, dx, dy, n, u, v, side = "r"):
        """
            w: width
            h: height
            d: dis between lines
            l: len of line
            n: nth line
            v: value
            u: each line sperate's value MEIYIGE JIANGE DAIBIAODE ZHI
        """

        if side == "r":
            return (
                w - l + dx,
                ((v % u) / u + n) * d + 0.5 * h + dy,
                w - 1 + dx,
                ((v % u) / u + n) * d + 0.5 * h + dy
            )
        else:
            return (
                dx,
                ((v % u) / u + n) * d + 0.5 * h + dy,
                l + dx,
                ((v % u) / u + n) * d + 0.5 * h + dy
            )
            

    def _rollbar_num_val(self, v, u, n):
        return v - (v % u) - n * u
        

if __name__ == "__main__":
    P = PFD()
    P.run()
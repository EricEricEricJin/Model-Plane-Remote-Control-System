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

    """Recommanded H:W: 16:10"""

    WIN_H = 640
    WIN_W = 400

    STA_IND_H = int(WIN_H / 16)
    STA_IND_W = WIN_W
    STA_IND_X = 0
    STA_IND_Y = 0
    
    SPEED_H = int(WIN_H / 3.2)
    SPEED_W = int(WIN_W / 5)
    SPEED_X = 0
    SPEED_Y = STA_IND_H

    ATT_A = int(min(WIN_H / 3.2, WIN_W / 2))
    ATT_X, ATT_Y = int(9 / 20 * WIN_W - 1 / 2 * ATT_A), int(7 / 32 * WIN_H - 1 / 2 * ATT_A)

    ALT_H = SPEED_H
    ALT_W = SPEED_W
    ALT_X = 7 / 10 * WIN_W
    ALT_Y = SPEED_Y

    VS_H = SPEED_H
    VS_W = int(SPEED_W / 2)
    VS_X = 9 / 10 * WIN_W
    VS_Y = SPEED_Y

    HDG_A = int(min(0.625 * WIN_H, WIN_W))
    HDG_X = 1 / 2 * (WIN_W - HDG_A)
    HDG_Y = SPEED_Y + SPEED_H + (WIN_H - SPEED_H - STA_IND_H - HDG_A) / 2

    def __init__(self):
        # self.COM = Communicate()
        # self.COM.send(b"pfd")

        self.root = Tk()
        self.root.geometry(str(self.WIN_W) + "x" + str(self.WIN_H))
        # self.root.overrideredirect(True)

        self.sta_ind_cvs = Canvas(master = self.root, height = self.STA_IND_H, width = self.STA_IND_W, bg = "black", highlightthickness = 0)
        self.sta_ind_cvs.place(x = self.STA_IND_X, y = self.STA_IND_Y)
        
        self.speed_cvs = Canvas(master = self.root, height = self.SPEED_H, width = self.SPEED_W, bg = "black", highlightthickness = 0)
        self.speed_cvs.place(x = self.SPEED_X, y = self.SPEED_Y)

        self.att_cvs = Canvas(master = self.root, height = self.ATT_A, width = self.ATT_A, bg = "black", highlightthickness = 0)
        self.att_cvs.place(x = self.ATT_X, y = self.ATT_Y)

        self.alt_cvs = Canvas(master = self.root, height = self.ALT_H, width = self.ALT_W, bg = "black", highlightthickness = 0)
        self.alt_cvs.place(x = self.ALT_X, y = self.ALT_Y)

        self.vs_cvs = Canvas(master = self.root, height = self.VS_H, width = self.VS_W, bg = "black", highlightthickness = 0)
        self.vs_cvs.place(x = self.VS_X, y = self.VS_Y)

        self.hdg_cvs = Canvas(master = self.root, height = self.HDG_A, width = self.HDG_A, bg = "black", highlightthickness = 0)
        self.hdg_cvs.place(x = self.HDG_X, y = self.HDG_Y)
        # NOTE: buyao yongman h

        self._init_speed()
        self._init_att()
        self._init_alt()
        self._init_vs()


    def _init_speed(self):
        self.speed_lines = []
        self.speed_texts = []

        self.speed_cvs.create_rectangle(1 / 4 * self.SPEED_W, 0, 3 / 4 * self.SPEED_W, self.SPEED_H, fill = "grey")

        for i in range(16):
            self.speed_lines.append(self.speed_cvs.create_line(-114, -114, -114, -114, fill = "white"))
            self.speed_texts.append(self.speed_cvs.create_text(-114, -114, text = "0", fill = "white"))
        
        self.speed_cvs.create_polygon((1 / 8 * self.SPEED_W, 9 / 20 * self.SPEED_H, 5 / 8 * self.SPEED_W, 9 / 20 * self.SPEED_H, 3 / 4 * self.SPEED_W, 1 / 2 * self.SPEED_H, 5 / 8 * self.SPEED_W, 11 / 20 * self.SPEED_H, 1 / 8 * self.SPEED_W, 11 / 20 * self.SPEED_H), fill = "#202020")
        self.speed_val_text = self.speed_cvs.create_text(3 / 8 * self.SPEED_W, 1 / 2 * self.SPEED_H, text = "", fill = "white")

        self.accel_indi = self.speed_cvs.create_rectangle(3 / 4 * self.SPEED_W, 1 / 2 * self.SPEED_H, 4 / 5 * self.SPEED_W, 1 / 2 * self.SPEED_H, fill = "white")

    def _init_att(self):        
        self.blue_poly = self.att_cvs.create_rectangle((0, 0, self.ATT_A, self.ATT_A), fill = "blue", width = 0)
        self.brown_poly = self.att_cvs.create_polygon((-114, -114, -114, -114), fill = "red")

        self.att_lines = []
        self.att_texts = []

        for i in range(25):
            self.att_lines.append(self.att_cvs.create_line(-114, -114, -114, -114, fill = "white"))

        for i in range(13):
            self.att_texts.append(self.att_cvs.create_text(-114, -114, text = str(abs(60 - 10 * i)) ))
            self.att_texts.append(self.att_cvs.create_text(-114, -114, text = str(abs(60 - 10 * i)) ))

        self.att_cvs.create_line(3 / 10 * self.ATT_A, 1 / 2 * self.ATT_A, 9 / 20 * self.ATT_A, 1 / 2 * self.ATT_A, width = 5, fill = "black")
        self.att_cvs.create_line(11 / 20 * self.ATT_A, 1 / 2 * self.ATT_A, 7 / 10 * self.ATT_A, 1 / 2 * self.ATT_A, width = 5, fill = "black")
        self.att_cvs.create_rectangle(49 / 100 * self.ATT_A, 49 / 100 * self.ATT_A, 51 / 100 * self.ATT_A, 51 / 100 * self.ATT_A, fill = "black")

    def _init_alt(self):
        self.alt_lines = []
        self.alt_texts = []

        self.alt_cvs.create_rectangle(1 / 4 * self.ALT_W, 0, 3 / 4 * self.ALT_W, self.ALT_H, fill = "grey")

        for i in range(16):
            self.alt_lines.append(self.alt_cvs.create_line(-114, -114, -114, -114, fill = "white"))
            self.alt_texts.append(self.alt_cvs.create_text(-114, -114, text = "0", fill = "white"))

        self.alt_cvs.create_polygon((1 / 4 * self.ALT_W, 1 / 2 * self.ALT_H, 3 / 8 * self.ALT_W, 11 / 20 * self.ALT_H, 7 / 8 * self.ALT_W, 11 / 20 * self.ALT_H, 7 / 8 * self.ALT_W, 9 / 20 * self.ALT_H, 3 / 8 * self.ALT_W, 9 / 20 * self.ALT_H), fill = "#202020")
        self.alt_val_text = self.alt_cvs.create_text(5 / 8 * self.ALT_W, 1 / 2 * self.ALT_H, text = "", fill = "white")

    def _init_vs(self):
        self.vs_cvs.create_polygon((1 / 4 * self.VS_W, 0, 1 / 4 * self.VS_W, self.VS_H, 3 / 4 * self.VS_W, 39 / 40 * self.VS_H, 3 / 4 * self.VS_W, 1 / 40 * self.VS_H), fill = "grey")
        # (40, 200-780tan(0.04083v)) # Fuck magic numbers
        for i in range(-5, 6):
            # self.vs_cvs.create_text(40, 200-780 * math.tan(0.04083 * i), text = str(abs(i)), fill = "white")
            l_cd = self._vs_line_coord(i * 100)
            self.vs_cvs.create_text((l_cd[0] + l_cd[2]) / 2, (l_cd[1] + l_cd[3]) / 2, text = str(abs(i)))
        self.vs_line = self.vs_cvs.create_line(-114, -114, -114, -114, width = self.VS_H / 100)

    def _init_hdg(self):
        pass

    def run(self):
        t = Thread(target = self._service)
        t.start()

        self.root.mainloop()

    def _service(self):
        while True:
            # raw = self.COM.recv()
            # speed, pitch, roll, alt, vs, hdg, lat, lon, tar_lat, tar_lon, tar_dir = unpack("", raw)
            speed, accel, pitch, roll, alt, vs, hdg, lat, lon, tar_lat, tar_lon, tar_dir = 14, 10, 10, 10, 10, 400, 10, 10, 10, 10, 10, 10
            speed = 650
            roll = 20
            pitch = -10
            alt = 10000
            vs = -800

            self._update_speed(speed, accel)
            self._update_att(pitch, roll)
            self._update_alt(alt)
            self._update_vs(vs)

    def _update_speed(self, speed, accel):
        self.speed_cvs.itemconfigure(self.speed_val_text, text = str(speed))

        for i in range(16):
            self.speed_cvs.coords(self.speed_lines[i], self._rollbar_line_coord(self.SPEED_W / 2, self.SPEED_H, self.SPEED_H / 16, 1 / 4 * self.SPEED_W - 1 / 8 * self.SPEED_W * (i % 2), 1 / 4 * self.SPEED_W, 0, i - 8, 5, speed))
            if i % 2 == 0:
                self.speed_cvs.coords(self.speed_texts[int(i / 2)], (3 / 8 * self.SPEED_W, self._rollbar_line_coord(1 / 2 * self.SPEED_W, self.SPEED_H, 1 / 16 * self.SPEED_H, 1 / 4 * self.SPEED_W, 1 / 4 * self.SPEED_W, 0, i - 8, 5, speed)[1]))
                self.speed_cvs.itemconfigure(self.speed_texts[int(i / 2)], text = str(self._rollbar_num_val(speed, 5, i - 8)))
        
        self.speed_cvs.coords(self.accel_indi, (3 / 4 * self.SPEED_W, 1 / 2 * self.SPEED_H, 4 / 5 * self.SPEED_W, 1 / 2 * self.SPEED_H - accel * (self.SPEED_H / 40)))

    def _update_att(self, pitch, roll):
        long_center_line_coord = self._att_line_coord(self.ATT_A, roll, pitch, 2 * 1.42 * 13 / 8 * self.ATT_A, 1 / 8 * self.ATT_A, 0, 5)
        print("LCLC: ", long_center_line_coord)

        if 45 < roll <= 135:
            # left
            brown_coord = (
                long_center_line_coord[0], long_center_line_coord[1], 
                long_center_line_coord[2], long_center_line_coord[3],
                0, self.ATT_A,
                0, 0
            )
            
        elif 135 < roll <= 180 or -180 < roll <= -135:
            # up
            brown_coord = (
                long_center_line_coord[0], long_center_line_coord[1], 
                long_center_line_coord[2], long_center_line_coord[3],
                0, 0,
                self.ATT_A, 0
            )
            pass
        elif -135 < roll <= -45:
            # right
            brown_coord = (
                long_center_line_coord[0], long_center_line_coord[1], 
                long_center_line_coord[2], long_center_line_coord[3],
                self.ATT_A, 0,
                self.ATT_A, self.ATT_A
            )

            pass
        elif -45 < roll <= 45:
            # down
            brown_coord = (
                long_center_line_coord[0], long_center_line_coord[1], 
                long_center_line_coord[2], long_center_line_coord[3],
                self.ATT_A, self.ATT_A,
                0, self.ATT_A
            )

        self.att_cvs.coords(self.brown_poly, (brown_coord))

        for i in range(25):
            coord = self._att_line_coord(self.ATT_A, roll, pitch, 3 / 8 * self.ATT_A - (i % 2) * 1 / 8 * self.ATT_A, 1 / 8 * self.ATT_A, i - 12, 5)
            self.att_cvs.coords(self.att_lines[i], 
                coord
            )
            if i % 2 == 0:
                self.att_cvs.coords(self.att_texts[i], (coord[0] - math.cos(math.radians(roll)) * 1 / 40 * self.ATT_A, coord[1] - math.sin(math.radians(roll)) * 1 / 40 * self.ATT_A))
                self.att_cvs.coords(self.att_texts[i + 1], (coord[2] + math.cos(math.radians(roll)) * 1 / 40 * self.ATT_A, coord[3] + math.sin(math.radians(roll)) * 1 / 40 * self.ATT_A))
        
        for i in range(26):
            self.att_cvs.itemconfigure(self.att_texts[i], angle = -roll)

    def _update_alt(self, alt):
        self.alt_cvs.itemconfigure(self.alt_val_text, text = str(alt))

        for i in range(16):
            self.alt_cvs.coords(self.alt_lines[i], self._rollbar_line_coord(self.ALT_W / 2, self.ALT_H, 1 / 16 * self.ALT_H, 1 / 4 * self.ALT_W - 1 / 8 * self.ALT_W * (i % 2), 1 / 4 * self.ALT_W, 0, i - 8, 5, alt, side = "l"))
            if i % 2 == 0:
                self.alt_cvs.coords(self.alt_texts[int(i / 2)], (5 / 8 * self.ALT_W, self._rollbar_line_coord(self.ALT_W / 2, self.ALT_H, 1 / 16 * self.ALT_H, 1 / 4 * self.ALT_W, 1 / 4 * self.ALT_W, 0, i - 8, 5, alt, side = "l")[1]))
                self.alt_cvs.itemconfigure(self.alt_texts[int(i / 2)], text = str(self._rollbar_num_val(alt, 5, i - 8)))

    def _update_vs(self, vs):
        self.vs_cvs.coords(self.vs_line, self._vs_line_coord(vs))
        if abs(vs) <= 300:
            color = "green"
        elif 300 < abs(vs) <= 600:
            color = "yellow"
        elif abs(vs) > 600:
            color = "red"
        self.vs_cvs.itemconfigure(self.vs_line, fill = color)





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
        
    def _vs_line_coord(self, v):
        if v > 600:
            v = 600
        elif v < -600:
            v = -600
        
        return (
            1 / 4 * self.VS_W, 1 / 2 * self.VS_H - 10 * self.VS_W * math.tan(v / 600 * math.atan(self.VS_H / (20 * self.VS_W))),
            3 / 4 * self.VS_W, 1 / 2 * self.VS_H - 19 / 2 * self.VS_W * math.tan(v / 600 * math.atan(self.VS_H / (20 * self.VS_W)))
        )
        
        """
            return (
                20, 200 - 800 * math.tan(0.0004083 * v),
                60, 200 - 760 * math.tan(0.0004083 * v)
            )
            # Fucking magic numbers when 80x400
        """

if __name__ == "__main__":
    P = PFD()
    P.run()
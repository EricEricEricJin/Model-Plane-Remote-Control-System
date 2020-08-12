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
from time import sleep
from com import Communicate

class updateTest:
    def __init__(self):
        self.data_list = {
            "pitch": 0, "roll": 0, 
            "air_speed": 0, "gnd_speed": 0, "accel": 0,
            "psr_alt": 0, "tof_alt": 0,"vs": 0,
            "hdg": 0,
            "long": 0, "lat": 0,
            "FD_ON": True, 
            "tar_speed": 10, "tar_alt": -10, "tar_hdg": 0, "tar_long": 0, "tar_lat": 0,
            "sta" : {
                "CRUISE": True, "MANU": True, "FAC": True, "AP_HDG": True,
                "TO/LD": True, "AUTO": True, "MCAS": True, "AP_ALT": True,
                "AP_SPD": True
            }
        }
        self.P = PFD()
        


    def run(self):
        t = Thread(target = self._service)
        t.start()
        self.P.run()

    def _service(self):
        while True:
            self.data_list["pitch"] += 1
            self.P.update(self.data_list)
            sleep(1)




class PFD:

    """Recommanded H:W: 16:10"""

    WIN_H = 1200
    WIN_W = 800

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
        self.data_list = {}
        
        # self.COM = Communicate()
        # self.COM.send(b"pfd")

        self.root = Tk()
        self.root.geometry(str(self.WIN_W) + "x" + str(self.WIN_H))
        self.root.configure(bg = "black")
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

        self._init_sta_ind()
        self._init_speed()
        self._init_att()
        self._init_alt()
        self._init_vs()
        self._init_hdg()

    def _init_sta_ind(self):
        for i in range(3):
            coord = (
                self.STA_IND_W / 4 * (i + 1), 0, 
                self.STA_IND_W / 4 * (i + 1), self.STA_IND_H / 5 * 4
            )
            self.sta_ind_cvs.create_line(coord, fill = "white")

        self.sta_ind_disp_text = [
            ["CRUISE", "MANU", "FAC", "AP_HDG"],
            ["TO/LD", "AUTO", "MCAS", "AP_ALT"],
            ["", "", "", "AP_SPD"],
            ["", "", "", ""]
        ]

        self.sta_ind_disp_mat = []

        for i in range(4):
            self.sta_ind_disp_mat.append([])
            for j in range(4):
                coord = ((1 + 2 * j) / 8 * self.STA_IND_W, (1 + 2 * i) / 8 * self.STA_IND_H)
                self.sta_ind_disp_mat[i].append(self.sta_ind_cvs.create_text(coord, text = self.sta_ind_disp_text[i][j], fill = "black"))

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
        self.speed_fd = self.speed_cvs.create_polygon(-114, -114, -114, -114, outline = "pink")

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

        self.alt_fd = self.alt_cvs.create_polygon(-114, -114, -114, -114, outline = "pink")

    def _init_vs(self):
        self.vs_cvs.create_polygon((1 / 4 * self.VS_W, 0, 1 / 4 * self.VS_W, self.VS_H, 3 / 4 * self.VS_W, 39 / 40 * self.VS_H, 3 / 4 * self.VS_W, 1 / 40 * self.VS_H), fill = "grey")
        # (40, 200-780tan(0.04083v)) # Fuck magic numbers
        for i in range(-5, 6):
            # self.vs_cvs.create_text(40, 200-780 * math.tan(0.04083 * i), text = str(abs(i)), fill = "white")
            l_cd = self._vs_line_coord(i * 100)
            self.vs_cvs.create_text((l_cd[0] + l_cd[2]) / 2, (l_cd[1] + l_cd[3]) / 2, text = str(abs(i)))
        self.vs_line = self.vs_cvs.create_line(-114, -114, -114, -114, width = self.VS_H / 100)

    def _init_hdg(self):

        self.hdg_real_dis_betw_circ = 100 # ft
        self.hdg_delta_r_of_circ = self.HDG_A / 10

        # Plane sign
        self.hdg_cvs.create_polygon(
            self._hdg_planesign_coord(self.HDG_A / 2, self.HDG_A / 2, self.HDG_A / 100),
            outline = "white"
        )

        # Heading ray
        self.hdg_cvs.create_line(
            self.HDG_A / 2, self.HDG_A / 2 - 4 * self.hdg_delta_r_of_circ, 
            self.HDG_A / 2, self.HDG_A / 2 - self.HDG_A / 200,
            fill = "white"
        )

        # radar panel
        for i in range(1, 5):
            self.hdg_cvs.create_arc(self.HDG_A / 2 - i * self.hdg_delta_r_of_circ, self.HDG_A / 2 - i * self.hdg_delta_r_of_circ, self.HDG_A / 2 + i * self.hdg_delta_r_of_circ, self.HDG_A / 2 + i * self.hdg_delta_r_of_circ, start = 270, extent = 359, outline = "white", style = ARC)
            if i < 4:
                self.hdg_cvs.create_text(self.HDG_A / 2 - i * self.hdg_delta_r_of_circ - 10, self.HDG_A / 2, text = str(i), fill = "white")

        self.hdg_line_num = 72
        self.hdg_line_list = []
        self.hdg_text_list = []

        # lines KEDU
        for i in range(self.hdg_line_num):
            self.hdg_line_list.append(self.hdg_cvs.create_line(-114, -114, -114, -114, fill = "white"))
            if i % 2 == 0:
                self.hdg_text_list.append(self.hdg_cvs.create_text(-114, -114, text = str(int(i * 360 / self.hdg_line_num)), fill = "white"))

        self.hdg_cvs.create_polygon(
            self._hdg_numbox_coord(self.HDG_A / 2, self.HDG_A / 2 - 4 * self.hdg_delta_r_of_circ, self.HDG_A / 16),
            outline = "white"
        )

        self.hdg_val_text = self.hdg_cvs.create_text(self.HDG_A / 2, self.HDG_A / 2 - 4 * self.hdg_delta_r_of_circ - self.HDG_A / 32, text = "", fill = "white")

        # self.hdg_fd = 



        

    def run(self):
        # t = Thread(target = self._service)
        # t.start()
        self.root.after(50, self._service)
        self.root.mainloop()

    def update(self, data_list):
        self.data_list = data_list

    def _service(self):
        try:
            self._update_sta_ind(self.data_list["sta"])
            self._update_speed(self.data_list["air_speed"], self.data_list["accel"], self.data_list["FD_ON"], self.data_list["tar_speed"])
            self._update_att(self.data_list["pitch"], self.data_list["roll"])
            self._update_alt(self.data_list["psr_alt"], self.data_list["FD_ON"], self.data_list["tar_alt"])
            self._update_vs(self.data_list["vs"])
            self._update_hdg(16)
            
            
            self.root.after(100, self._service)

        except Exception as e:
            print(e)
            pass

    def _update_sta_ind(self, sta_dict):
        print(sta_dict)
        for i in range(len(self.sta_ind_disp_mat)):
            for j in range(len(self.sta_ind_disp_mat[i])):
                if self.sta_ind_disp_text[i][j] != "":
                    color = "green" if sta_dict[self.sta_ind_disp_text[i][j]] else "black"
                    self.sta_ind_cvs.itemconfigure(self.sta_ind_disp_mat[i][j], fill = color)

    def _update_speed(self, speed, accel, fd_on, tar_speed):
        self.speed_cvs.itemconfigure(self.speed_val_text, text = str(speed))

        for i in range(16):
            if i % 2:
                is_short = (speed % 10 < 5)
            else:
                is_short = not(speed % 10 < 5)
            self.speed_cvs.coords(self.speed_lines[i], self._rollbar_line_coord(self.SPEED_W / 2, self.SPEED_H, self.SPEED_H / 16, 1 / 4 * self.SPEED_W - 1 / 8 * self.SPEED_W * is_short, 1 / 4 * self.SPEED_W, 0, i - 8, 5, speed))
            if is_short == 0:
                self.speed_cvs.coords(self.speed_texts[int(i / 2)], (3 / 8 * self.SPEED_W, self._rollbar_line_coord(1 / 2 * self.SPEED_W, self.SPEED_H, 1 / 16 * self.SPEED_H, 1 / 4 * self.SPEED_W, 1 / 4 * self.SPEED_W, 0, i - 8, 5, speed)[1]))
                self.speed_cvs.itemconfigure(self.speed_texts[int(i / 2)], text = str(self._rollbar_num_val(speed, 5, i - 8)))
        
        self.speed_cvs.coords(self.accel_indi, (3 / 4 * self.SPEED_W, 1 / 2 * self.SPEED_H, 4 / 5 * self.SPEED_W, 1 / 2 * self.SPEED_H - accel * (self.SPEED_H / 40)))

        if fd_on:
            self.speed_cvs.coords(
                self.speed_fd, self._rollbar_fd_coord(
                    (3 / 4 * self.SPEED_W, self.SPEED_H / 2 - (tar_speed - speed) * self.SPEED_H / 80),
                    self.SPEED_W / 10
                )
            )
        else:
            self.speed_cvs.coords(self.speed_fd, (-114, -114, -114, -114))

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

    def _update_alt(self, alt, fd_on, tar_alt):
        self.alt_cvs.itemconfigure(self.alt_val_text, text = str(alt))

        for i in range(16):
            if i % 2:
                is_short = alt % 10 < 5
            else:
                is_short = not(alt % 10 < 5)

            self.alt_cvs.coords(self.alt_lines[i], self._rollbar_line_coord(self.ALT_W / 2, self.ALT_H, 1 / 16 * self.ALT_H, 1 / 4 * self.ALT_W - 1 / 8 * self.ALT_W * is_short, 1 / 4 * self.ALT_W, 0, i - 8, 5, alt, side = "l"))
            
            if is_short == 0:
                
                self.alt_cvs.coords(self.alt_texts[int(i / 2)], (5 / 8 * self.ALT_W, self._rollbar_line_coord(self.ALT_W / 2, self.ALT_H, 1 / 16 * self.ALT_H, 1 / 4 * self.ALT_W, 1 / 4 * self.ALT_W, 0, i - 8, 5, alt, side = "l")[1]))
                self.alt_cvs.itemconfigure(self.alt_texts[int(i / 2)], text = str(self._rollbar_num_val(alt, 5, i - 8)))
            
        if fd_on:
            self.alt_cvs.coords(
                self.alt_fd, 
                self._rollbar_fd_coord(
                    (1 / 4 * self.ALT_W, self.ALT_H / 2 - (tar_alt - alt) * self.ALT_H / 80),
                    self.ALT_W / 10
                )
            )
        else:
            self.alt_cvs.coords(self.alt_fd, (-114, -114, -114, -114))
        
    def _update_vs(self, vs):
        self.vs_cvs.coords(self.vs_line, self._vs_line_coord(vs))
        if abs(vs) <= 300:
            color = "green"
        elif 300 < abs(vs) <= 600:
            color = "yellow"
        elif abs(vs) > 600:
            color = "red"
        self.vs_cvs.itemconfigure(self.vs_line, fill = color)

    def _update_hdg(self, hdg):
        for i in range(self.hdg_line_num):
            if i % 2:
                # short
                coord = self._hdg_line_coord(4 * self.hdg_delta_r_of_circ, 3.8 * self.hdg_delta_r_of_circ, 360 / self.hdg_line_num, self.HDG_A / 2, self.HDG_A / 2, i, hdg)
            else:
                # long
                coord = self._hdg_line_coord(4 * self.hdg_delta_r_of_circ, 3.6 * self.hdg_delta_r_of_circ, 360 / self.hdg_line_num, self.HDG_A / 2, self.HDG_A / 2, i, hdg)
                
                coord_t = self._hdg_line_coord(4.2 * self.hdg_delta_r_of_circ, 4 * self.hdg_delta_r_of_circ, 360 / self.hdg_line_num, self.HDG_A / 2, self.HDG_A / 2, i, hdg)[0:2]
                self.hdg_cvs.coords(
                    self.hdg_text_list[int(i / 2)],
                    coord_t
                )
                self.hdg_cvs.itemconfigure(
                    self.hdg_text_list[int(i / 2)],
                    angle = hdg - i * 360 / self.hdg_line_num
                )

            self.hdg_cvs.coords(
                self.hdg_line_list[i],
                coord
            )
        
        self.hdg_cvs.itemconfigure(self.hdg_val_text, text = str(hdg))
            


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

    def _rollbar_fd_coord(self, o, a):
        """
            o: (x, y) or origin point
            a: side length
        """
        return (
            o[0] - a / 2, o[1] - a / 2,
            o[0] + a / 2, o[1] - a / 2,
            o[0] + a / 2, o[1] - 3 / 10 * a,
            o[0] + a / 4, o[1] - 1 / 10 * a,
            o[0] + a / 4, o[1] + 1 / 10 * a,
            o[0] + a / 2, o[1] + 3 / 10 * a,
            o[0] + a / 2, o[1] + a / 2,
            o[0] - a / 2, o[1] + a / 2,
            o[0] - a / 2, o[1] + 3 / 10 * a,
            o[0] - a / 4, o[1] + 1 / 10 * a,
            o[0] - a / 4, o[1] - 1 / 10 * a,
            o[0] - a / 2, o[1] - 3 / 10 * a
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

    def _hdg_line_coord(self, R, r, d, xo, yo, n, v):
        """
            R: Big circle radi
            r: Samll circle radi
            d: deg between two line
            xo: center x
            yo: center y
            n: nth line
            v: value(deg)
        """

        theta = n * d - v
        
        return (
            xo + math.sin(math.radians(theta)) * R, yo - math.cos(math.radians(theta)) * R,
            xo + math.sin(math.radians(theta)) * r, yo - math.cos(math.radians(theta)) * r
        )

    def _hdg_num_val(self, v, d, n):
        """
            v: hdg in deg
            d: deg diff between lines
            n: nth number
        """

        return n * d

    def _hdg_planesign_coord(self, xo, yo, a):
        return (
            xo, yo - a,
            xo + a / 2, yo - a / 4,
            xo + a / 2, yo + a,
            xo - a / 2, yo + a,
            xo - a / 2, yo - a / 4,
        )

    def _hdg_numbox_coord(self, x, y, a):
        return (
            x, y,
            x + a / 2, y - a / 4,
            x + a / 2, y - a / 3 * 2,
            x - a / 2, y - a / 3 * 2,
            x - a / 2, y - a / 4
        )

    def _hdg_fd_coord(self, xo, yo, r, deg):
        # 
        pass
    
if __name__ == "__main__":
    UT = updateTest()
    UT.run()
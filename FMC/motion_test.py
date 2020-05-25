from motion import Motion
M = Motion()
while True:
    cmd = input("> ")
    if cmd == 0:
        M.change_pwr(0, 0)
    else:
        p = cmd.split(" ")
        M.change_pwr(int(p[0]), int(p[1]))

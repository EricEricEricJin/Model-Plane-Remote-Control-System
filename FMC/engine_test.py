from motions.engine import Engine
if __name__ == "__main__":
    E = Engine()
    E.init()
    while True:
        pwr = int(input("pwr: "))
        if pwr == 114514:
            break
        E.change_pwr(pwr)
    del(E)
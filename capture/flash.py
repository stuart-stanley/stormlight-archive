import obl
import time

if __name__ == '__main__':
    sl = obl.Stormlight()
    while True:
        sl.all_to(255,255,255)
        time.sleep(0.2)
        sl.all_to(0,0,0)
        time.sleep(0.2)


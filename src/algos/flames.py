import random


class Flames(object):
    def __init__(self, display, count, duration):
        self.__display = display
        self.__count = count
        self.__duration = duration
        self.__r = 226
        self.__g = 8
        self.__b = 35

    def tick_cb(self):
        for inx in range(0, self.__count / 2):
            flicker = random.randint(0, 55)
            r1 = self.__r - flicker
            g1 = self.__g - flicker
            b1 = self.__b - flicker
            x_r = inx
            x_l = 99 - inx  # todo: length from where?
            for z in range(0, 2):
                self.__display.set_pixel((x_r, 0, z), None, (r1, g1, b1))
                self.__display.set_pixel((x_l, 0, z), None, (r1, g1, b1))

        if self.__duration == 0:
            import sys
            sys.exit(0)
        self.__duration -= 1
        if self.__duration % 1000 == 0:
            print self.__duration

        self.__display.refresh_physical()

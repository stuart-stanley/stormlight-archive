
from .algo_utils import XYZVelocity, MovingPixel, SimpleXYZVelocity
import random


class TreeCircle(object):
    def __init__(self, display, location, rgb_color, velocity, tail_len):
        assert isinstance(velocity, XYZVelocity)
        assert len(location) == 3
        assert len(rgb_color) == 3
        assert tail_len > 0
        r, g, b = rgb_color
        ir, ig, ib = rgb_color

        pix_list = []
        for inx in range(0, tail_len):
            new_pixel = MovingPixel(display, location, velocity, (r, g, b))
            for pixel in pix_list:
                pixel.do_move()
            pix_list.append(new_pixel)
            r = int(ir / (inx + 2))
            g = int(ig / (inx + 2))
            b = int(ib / (inx + 2))

        self.__pixels = pix_list

    def tick_cb(self):
        for pixel in self.__pixels:
            pixel.tick_cb()


class TreeCircleGroup(object):
    def __init__(self, display, count, duration):
        ffl = []
        for inx in range(0, count):
            dxt = random.randint(1, 10)
            mv = random.choice([-1, 1])
            tail = random.randint(3, 10)
            t = 255
            r = random.randint(0, 255)
            t -= r
            g = random.randint(0, t)
            t -= g
            b = random.randint(0, t)
            x = random.randint(0, 99)
            z = random.randint(0, 1)
            y = 0
            vel = SimpleXYZVelocity(display, dxt, 0, 0, mv, 0, 0)  # XXX ick
            ff = TreeCircle(display, (x, y, z), (r, g, b), vel, tail)
            ffl.append(ff)
        self.__fireflys = ffl
        self.__display = display
        self.__duration = duration

    def tick_cb(self):
        for ff in self.__fireflys:
            ff.tick_cb()

        if self.__duration == 0:
            import sys
            sys.exit(0)
        self.__duration -= 1
        if self.__duration % 1000 == 0:
            print(self.__duration)

        self.__display.refresh_physical()


class TestTreeCircle(object):
    def __init__(self, display):
        slow = SimpleXYZVelocity(display, 1, 0, 0, 1, 0, 0, xb=False)
        fast = SimpleXYZVelocity(display, 10, 0, 0, 1, 0, 0)
        ffslow = TreeCircle(display, (50, 0, 0), (255, 0, 0), slow, 5)
        self.__fireflys = [ffslow]
        if False:
            fffast = TreeCircle(display, (0, 0, 0), (0, 255, 0), fast, 8)
            self.__fireflys.append(fffast)

        if False:
            med = SimpleXYZVelocity(display, 2, 0, 2, 1, 0, 1)
            fmed = TreeCircle(display, (80, 0, 0), (0, 0, 255), med, 20)
            self.__fireflys.append(fmed)
        self.__display = display

    def tick_cb(self):
        for ff in self.__fireflys:
            ff.tick_cb()
        self.__display.refresh_physical()

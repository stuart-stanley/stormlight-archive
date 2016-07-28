
from .algo_utils import XYZVelocity, MovingPixel, SimpleXYZVelocity, Velocity
import random


class FireFly(object):
    def __init__(self, display, location, rgb_color, velocity, tail_len):
        assert isinstance(velocity, XYZVelocity)
        assert len(location) == 3
        assert len(rgb_color) == 3
        assert tail_len > 0
        r, g, b = rgb_color
        ir, ig, ib = rgb_color

        pix_list = []
        for inx in range(0, tail_len):
            new_pixel = MovingPixel(display, location, velocity, (r,g,b))
            for pixel in pix_list:
                pixel.do_move()
            pix_list.append(new_pixel)
            r = ir / (inx + 2)
            g = ig / (inx + 2)
            b = ib / (inx + 2)

        self.__pixels = pix_list

    def tick_cb(self):
        for pixel in self.__pixels:
            pixel.tick_cb()

class FireFlyGroup(object):
    def __init__(self, display, count):
        ffl = []
        for inx in range(0, count):
            dxt = random.randint(1, 10)
            mv = random.choice([-1, 1])
            tail = random.randint(3,10)
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            x = random.randint(0,99)
            z = random.randint(0,1)
            y = 0
            vel = SimpleXYZVelocity(display, dxt, 0, 0, mv, 0, 0) # XXX ick
            ff = FireFly(display, (x, y, z), (r, g, b), vel, tail)
            ffl.append(ff)
        self.__fireflys = ffl
        self.__display = display

    def tick_cb(self):
        for ff in self.__fireflys:
            ff.tick_cb()
        self.__display.refresh_physical()
            
            
class TestFly(object):
    def __init__(self, display):
        ffl = []
        slow = SimpleXYZVelocity(display, 10, 0, 0, 1, 0, 0)
        fast = SimpleXYZVelocity(display, 1, 0, 0, 1, 0, 0)
        ffslow = FireFly(display, (50, 0, 0), (255, 0, 0), slow, 5)
        fffast = FireFly(display, (0, 0, 0), (0, 255, 0), fast, 8)
        self.__fireflys = [ffslow, fffast]
        if True:
            med = SimpleXYZVelocity(display, 2, 0, 2, 1, 0, 1)
            fmed = FireFly(display, (80, 0, 0), (0, 0, 255), med, 20)
            self.__fireflys.append(fmed)
        self.__display = display

    def tick_cb(self):
        for ff in self.__fireflys:
            ff.tick_cb()
        self.__display.refresh_physical()
           
 


from .algo_utils import XYZVelocity, MovingPixel, SimpleXYZVelocity, Velocity
import random


class FireFly(object):
    def __init__(self, display, location, rgb_color, velocity, tail_len):
        assert isinstance(velocity, XYZVelocity)
        assert len(location) == 3
        assert len(rgb_color) == 3
        assert tail_len > 0
        r, g, b = rgb_color

        pix_list = []
        for inx in range(0, tail_len):
            new_pixel = MovingPixel(display, location, velocity, (r,g,b))
            for pixel in pix_list:
                pixel.do_move()
            pix_list.append(new_pixel)
            r = r / 2
            g = g / 2
            b = b / 2

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

    def tick_cb(self, obj, event):
        for ff in self.__fireflys:
            ff.tick_cb()
        self.__display.refresh_physical()
            
            

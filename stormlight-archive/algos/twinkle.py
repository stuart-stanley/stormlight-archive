import random
import time
import sys

_debug = False

class ColorMigrate(object):
    def __init__(self, current, dim=1, cds=(1,1,1), low=(0,0,0)):
        lr, lg, lb = low
        r = random.randint(lr,255) * cds[0] * dim
        g = random.randint(lg,255) * cds[1] * dim
        b = random.randint(lb,255) * cds[2] * dim
        self.__tcolors = (r, g, b)
        cur_colors = []
        rates = []
        assert len(current) == 3, 'must be (r,g,b)'
        mx_delta = 0
        for inx in range(0,3):
            cur_color = float(current[inx])
            delta = float(self.__tcolors[inx] - current[inx]) 
            if delta > mx_delta:
                mx_delta = delta
            rate = (delta / 255.0) # * (random.random() + 0.75) * 4
            cur_colors.append(cur_color)
            rates.append(rate)
        self.__cur_colors = cur_colors
        self.__rates = rates
        self.__ticks_to_done = int(mx_delta)
        self.__dim = dim
        self.__cds = cds

        if _debug:
            print("init-cur", cur_colors, "rates", rates, "target", self.__tcolors, self.__ticks_to_done, "dim", dim)

    def color_tick(self):
        rl = []
        for inx in range(0,3):
            new_float_color = self.__cur_colors[inx] + self.__rates[inx]
            self.__cur_colors[inx] = new_float_color
            rl.append(int(new_float_color))
        self.__ticks_to_done -= 1
        if self.__ticks_to_done <= 0:
            rv = True
        else:
            rv = False
        if _debug:
            print("color-tick", self.__cur_colors, self.__rates, rl, rv, self.__ticks_to_done)
        return rv, rl

    def current_colors(self):
        rl = []
        for float_color in self.__cur_colors:
            rl.append(int(float_color))
        return rl

    def __str__(self):
        rs = "cc={}, ttd={}, tg={}, rt={}".format(
            self.__cur_colors, self.__ticks_to_done, self.__tcolors, self.__rates)
        return rs


class Twinkle(object):
    def __init__(self, display, count, duration):
        self.__display = display
        self.__count = count
        self.__duration = duration
        self.__max_dim = 0.5
        self.__dim = self.__max_dim
        self.__cdims = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        ]
        self.__ticks = 0
        self.__migrates = []
        self.__low = (32, 32, 32)
        self.__low = (0, 0, 0)
        for _ in range(count):
            self.__migrates.append(
                ColorMigrate((0,0,0), self.__dim, self.__skew_cdim(), self.__low))

    def __skew_cdim(self):
        return self.__cdims[random.randint(0, len(self.__cdims) - 1)]

    def tick_cb(self):
        self.__duration -= 1
        if self.__duration % 1000 == 0:
            print(self.__duration)
        self.__ticks += 1
        for inx in range(0, self.__count):
            migrate = self.__migrates[inx]
            if self.__ticks % 2 != 0:
                next_base_colors = migrate.current_colors()
            else:
                migrate_done, next_base_colors = migrate.color_tick()
                if migrate_done:
                    migrate = ColorMigrate(
                        next_base_colors, self.__dim, self.__skew_cdim(), self.__low)
                    self.__migrates[inx] = migrate
                    if self.__dim == 1:
                        self.__dim = 0
                    else:
                        self.__dim = self.__max_dim
                        if self.__duration < 0:
                            sys.exit(0)

            flicker = random.randint(0, 10)
            use_color = []
            for color in next_base_colors:
                color = color - flicker
                if color < 0:
                    color = 0
                if color > 255:
                    color = 255
                use_color.append(color)
            _debug = False
            if inx == 0 and _debug:
                print("pixel", inx, use_color, migrate)
            for z in range(0, 2):
                self.__display.set_pixel((inx, 0, z), None, use_color)
                self.__display.set_pixel((inx, 0, z), None, use_color)

        self.__display.refresh_physical()

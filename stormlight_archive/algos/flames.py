import random
import time
import sys

_debug = False


class ColorMigrate(object):
    def __init__(self, current, dim=1, cds=(1, 1, 1)):
        r = random.randint(0, 255) * cds[0] * dim
        g = random.randint(0, 255) * cds[1] * dim
        b = random.randint(0, 255) * cds[2] * dim
        self.__tcolors = (r, g, b)
        cur_colors = []
        rates = []
        assert len(current) == 3, 'must be (r,g,b)'
        for inx in range(0, 3):
            cur_color = float(current[inx])
            delta = float(self.__tcolors[inx] - current[inx])
            rate = delta / 255.0
            cur_colors.append(cur_color)
            rates.append(rate)
        self.__cur_colors = cur_colors
        self.__rates = rates
        self.__ticks_to_done = 255
        if _debug:
            print("init-cur", cur_colors, "rates", rates, "target", self.__tcolors, self.__ticks_to_done)

    def color_tick(self):
        rl = []
        for inx in range(0, 3):
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


class Flames(object):
    def __init__(self, display, count, duration):
        self.__display = display
        self.__count = count
        self.__duration = duration
        self.__max_dim = 0.25
        self.__dim = self.__max_dim
        self.__cdim = (1, 1, 1)
        self.__ticks = 0
        self.__migrate = ColorMigrate((0, 0, 0), self.__dim, self.__cdim)

    def tick_cb(self):
        self.__duration -= 1
        if self.__duration % 1000 == 0:
            print(self.__duration)
        self.__ticks += 1
        if self.__ticks % 1 != 0:
            time.sleep(0.1)
            next_base_colors = self.__migrate.current_colors()
        else:
            migrate_done, next_base_colors = self.__migrate.color_tick()
            if migrate_done:
                self.__migrate = ColorMigrate(next_base_colors, self.__dim, self.__cdim)
                if self.__dim == 1:
                    self.__dim = 0
                else:
                    self.__dim = self.__max_dim
                    if self.__duration < 0:
                        sys.exit(0)

        for inx in range(0, int(self.__count / 2)):
            flicker = random.randint(0, 55)
            use_color = []
            for color in next_base_colors:
                color = color - flicker
                if color < 0:
                    color = 0
                use_color.append(color)
            x_r = inx
            x_l = 99 - inx  # todo: length from where?
            if x_r == 0 and _debug:
                print("pixel", x_r, use_color)
            for z in range(0, 2):
                self.__display.set_pixel((x_r, 0, z), None, use_color)
                self.__display.set_pixel((x_l, 0, z), None, use_color)

        self.__display.refresh_physical()

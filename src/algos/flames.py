import random
import time


class ColorMigrate(object):
    def __init__(self, current, dim=1, cds=(1,1,1)):
        r = random.randint(0,255) * cds[0] * dim
        g = random.randint(0,255) * cds[1] * dim
        b = random.randint(0,255) * cds[2] * dim
        self.__tcolors = (r, g, b)
        cur_colors = []
        rates = []
        assert len(current) == 3, 'must be (r,g,b)'
        for inx in range(0,3):
            cur_color = float(current[inx])
            delta = float(self.__tcolors[inx] - current[inx])
            rate = delta / 255.0
            cur_colors.append(cur_color)
            rates.append(rate)
        self.__cur_colors = cur_colors
        self.__rates = rates
        self.__ticks_to_done = 255
        print "cur", cur_colors, "rates", rates, "target", self.__tcolors

    def color_tick(self):
        rl = []
        for inx in range(0,3):
            new_float_color = self.__cur_colors[inx] + self.__rates[inx]
            self.__cur_colors[inx] = new_float_color
            rl.append(int(new_float_color))
        self.__ticks_to_done -= self.__ticks_to_done
        if self.__ticks_to_done <= 0:
            rv = True
        else:
            rv = False
        return rv, rl

class Flames(object):
    def __init__(self, display, count, duration):
        self.__display = display
        self.__count = count
        self.__duration = duration
        self.__dim = 1
        self.__cdim = (1,1,1)
        self.__ticks = 0
        self.__migrate = ColorMigrate((0,0,0), self.__dim, self.__cdim)

    def tick_cb(self):
        if self.__duration == 0:
            import sys
            sys.exit(0)
        self.__duration -= 1
        if self.__duration % 1000 == 0:
            print self.__duration
        self.__ticks += 1
        if self.__ticks % 50 != 0:
            time.sleep(0.1)
            return

        migrate_done, next_base_colors = self.__migrate.color_tick()
        if migrate_done:
            self.__migrate = ColorMigrate(next_base_colors, self.__dim, self.__cdim)

        for inx in range(0, self.__count / 2):
            flicker = random.randint(0, 55)
            use_color = []
            for color in next_base_colors:
                color = color - flicker
                if color < 0:
                    color = 0
                use_color.append(color)
            x_r = inx
            x_l = 99 - inx  # todo: length from where?
            for z in range(0, 2):
                self.__display.set_pixel((x_r, 0, z), None, use_color)
                self.__display.set_pixel((x_l, 0, z), None, use_color)

        self.__display.refresh_physical()

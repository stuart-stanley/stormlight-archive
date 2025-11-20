import copy


class Velocity(object):
    def __init__(self, dt, increment=1, bounce=True):
        self.__dt = dt
        self.__increment = increment
        self.__limit = None
        self.__bounce = bounce
        self.__ticks = 0

    def set_limit(self, limit):
        assert self.__increment < limit
        self.__limit = limit

    def calculate_next(self, location):
        location += self.__increment
        if location >= self.__limit:
            if self.__bounce:
                self.__increment = -1 * self.__increment
                # went above limit implies increment was positive and is
                # now negative
                temp_inc = self.__increment - 1
                location += temp_inc
            else:
                location = location - self.__limit
        elif location < 0:
            if self.__bounce:
                self.__increment = -1 * self.__increment
                # went negative implies increment was negative and is now
                # positive
                temp_inc = self.__increment + 1
                location += temp_inc
            else:
                location = self.__limit = location
        assert location >= 0 and location < self.__limit, \
            'oops. location={0}, limit={1}'.format(location, self.__limit)
        return location

    def tick_cb(self, location):
        if self.__dt == 0:
            return location
        self.__ticks += 1
        if self.__ticks >= self.__dt:
            location = self.calculate_next(location)
            self.__ticks = 0
        return location


class XYZVelocity(object):
    def __init__(self, display, xdt, ydt, zdt):
        assert isinstance(xdt, Velocity)
        assert isinstance(ydt, Velocity)
        assert isinstance(zdt, Velocity)
        xdt.set_limit(display.max_x_pixel)
        ydt.set_limit(display.max_y_pixel)
        zdt.set_limit(display.max_z_pixel)
        self.__xdt = copy.copy(xdt)
        self.__ydt = copy.copy(ydt)
        self.__zdt = copy.copy(zdt)

    def calculate_next(self, location):
        x, y, z = location
        nx = self.__xdt.calculate_next(x)
        ny = self.__ydt.calculate_next(y)
        nz = self.__zdt.calculate_next(z)
        return (nx, ny, nz)

    def tick_cb(self, location):
        x, y, z = location
        nx = self.__xdt.tick_cb(x)
        ny = self.__ydt.tick_cb(y)
        nz = self.__zdt.tick_cb(z)
        return (nx, ny, nz)


class SimpleXYZVelocity(XYZVelocity):
    def __init__(self, display, xdt, ydt, zdt, xinc, yinc, zinc, xb=True, yb=True, zb=True):
        # TODO: bounce is really a property of the Arrangement?
        xdt = Velocity(xdt, xinc, bounce=xb)
        ydt = Velocity(ydt, yinc, bounce=yb)
        zdt = Velocity(zdt, zinc, bounce=zb)
        super(SimpleXYZVelocity, self).__init__(display, xdt, ydt, zdt)


class MovingPixel(object):
    def __init__(self, display, location, velocity, rgb_color):
        self.__display = display
        assert len(location) == 3
        self.__location = location
        self.__velocity = copy.deepcopy(velocity)
        self.__rgb_color = rgb_color

    def do_move(self):
        new_location = self.__velocity.calculate_next(self.__location)
        self.__location = new_location
        return new_location

    def tick_cb(self):
        new_location = self.__velocity.tick_cb(self.__location)
        if new_location != self.__location:
            self.__display.unset_pixel(self.__location, self)
            self.__display.set_pixel(new_location, self, self.__rgb_color)
            self.__location = new_location

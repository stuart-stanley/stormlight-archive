from collections import OrderedDict

# todo: ABC for all displays. Maybe auto-detect fake vs real
class LEDThing(object):
    def __init__(self, pos, sinx, linx, get_led_display_ctx_cb):
        self.__strand_index = sinx
        self.__led_index = linx
        self.__position = pos
        self.__red = 0
        self.__green = 0
        self.__blue = 0
        self.__modified = True
        self.__display_ctx = get_led_display_ctx_cb(self)
        self.__owned_by = OrderedDict()
        self.__dbg = False

    def __str__(self):
        rs = 'led(strand={0},linx={1},pos={2})'.format(
            self.__strand_index, self.__led_index, self.__position)
        return rs

    def __repr__(self):
        return str(self)

    def get_grid(self):
        return (self.__led_index, 0, self.__strand_index)

    def __calc_rgb_by_owners(self):
        r = 0
        g = 0
        b = 0
        for owner, rgb in self.__owned_by.items():
            wr, wg, wb = rgb
            r = (r + wr) & 0xff
            g = (g + wg) & 0xff
            b = (b + wb) & 0xff
        return r, g, b
            
    def set(self, red, green, blue, owner=None):
        if owner is not None:
            assert owner not in self.__owned_by.keys()
            self.__owned_by[owner] = (red, green, blue)
            red, green, blue = self.__calc_rgb_by_owners()
            
        if red != self.__red or green != self.__green or blue != self.__blue:
            self.__modified = True
        self.__red = red
        self.__green = green
        self.__blue = blue
        if self.__dbg:
            print("  {0} set to {1} owners={2}".format(
                self, (red, green, blue), len(self.__owned_by)))

    def unset(self, owner):
        if owner not in self.__owned_by.keys():
            print('warning: {0} missing from {1}'.format(owner, self.__owned_by))
        else:
            del self.__owned_by[owner]
            if self.__dbg:
                print("{0} owner {1} removed".format(self, owner))
        r, g, b = self.__calc_rgb_by_owners()
        self.set(r,g,b)

    def clear_modified(self):
        self.__modified = False

    @property
    def modified(self):
        return self.__modified

    @property
    def display_context(self):
        return self.__display_ctx

    @property
    def red(self):
        return self.__red

    @property
    def green(self):
        return self.__green

    @property
    def blue(self):
        return self.__blue

    @property
    def x(self):
        return self.__position[0]

    @property
    def y(self):
        return self.__position[1]

    @property
    def z(self):
        return self.__position[2]

    @property
    def radius(self):
        return 6

class Gradient(object):
    def __init__(self, base, step):
        assert base >=0 and base <= 255
        assert step >= -254 and step <= 254
        self.__base = base
        self.__step = step
        self.__next_value = base

    def reset(self):
        self.__next_value = self.__base

    def next_value(self):
        rval = self.__next_value
        nval = rval + self.__step
        if nval < 0:
            nval = nval + 255
        elif nval > 255:
            nval = nval - 255
        self.__next_value = nval
        return rval
    

class StrandThing(object):
    def __init__(self, strand_inx, get_led_display_ctx_cb):
        self.__leds = []
        self.__strand_inx = strand_inx
        self.__modified = True # todo: optimize modified
        self.__get_led_display_ctx_cb = get_led_display_ctx_cb

    def add_led(self, led_pos):
        led_inx = len(self.__leds)
        led = LEDThing(led_pos, self.__strand_inx, led_inx, 
                       self.__get_led_display_ctx_cb)
        self.__leds.append(led)
        return led

    def refresh_physical(self, add_led_set_to_update_cb):
        for led in self.__leds:
            if led.modified:
                add_led_set_to_update_cb(led)
                led.clear_modified()
        self.__modified = False
        
    def set(self, inx, r, g, b):
        led = self.__leds[inx]
        led.set(r,g,b)
        if not self.__modified and led.modified:
            self.__modified = True

    def setall(self, r, g, b):
        for led_inx in range(0, len(self.__leds)):
            self.set(led_inx, r, g, b)

    def set_gradient(self, r_grad, g_grad, b_grad):
        r_grad.reset()
        g_grad.reset()
        b_grad.reset()
        for led_inx in range(0, len(self.__leds)):
            self.set(led_inx, r_grad.next_value(), g_grad.next_value(), 
                     b_grad.next_value())

    def clearall(self):
        self.setall(0,0,0)

    def get_led(self, inx):
        return self.__leds[inx]

class DisplayDriver(object):
    def __init__(self):
        self.__strands = []
        self.__locked = False
        self.__limits = None

    def lock(self):
        assert not self.__locked, 'tried to lock more than once'
        assert self.__limits is not None, 'tried to lock before set_limits'
        self.__locked = True

    def __check_unlocked(self):
        assert not self.__locked, 'tried to alter locked display'

    def __check_locked(self):
        assert self.__locked, 'tried to use display while unlocked'

    def set_limits(self, lx, ly, lz):
        self.__check_unlocked()
        self.__limits = (lx, ly, lz)

    @property
    def max_x_pixel(self):
        return self.__limits[0]
    @property
    def max_y_pixel(self):
        return self.__limits[1]
    @property
    def max_z_pixel(self):
        return self.__limits[2]

    def add_strand(self):
        self.__check_unlocked()
        sinx = len(self.__strands)
        strand = StrandThing(sinx, self._led_display_context)
        self.__strands.append(strand)
        return strand

    def refresh_physical(self):
        self.__check_locked()
        self._start_update()
        for strand in self.__strands:
            strand.refresh_physical(self._add_set_to_update)
        self._complete_update()

    def setall(self, r, g, b):
        self.__check_locked()
        for strand in self.__strands:
            strand.setall(r,g,b)
        self.refresh_physical()

    def set_gradient(self, r_grad, g_grad, b_grad):
        self.__check_locked()
        assert isinstance(r_grad, Gradient)
        assert isinstance(g_grad, Gradient)
        assert isinstance(b_grad, Gradient)
        for strand in self.__strands:
            strand.set_gradient(r_grad, g_grad, b_grad)
        self.refresh_physical()

    def clearall(self):
        self.__check_locked()
        for strand in self.__strands:
            strand.clearall()
        self.refresh_physical()

    def __led_from_grid_location(self, grid_loc):
        gx, gy, gz = grid_loc
        assert gz < len(self.__strands) and gz >= 0
        assert gy == 0
        strand = self.__strands[gz]
        led = strand.get_led(gx)
        return led

    def unset_pixel(self, grid_loc, owner):
        led = self.__led_from_grid_location(grid_loc)
        led.unset(owner)

    def set_pixel(self, grid_loc, owner, rgb_color):
        led = self.__led_from_grid_location(grid_loc)
        r, g, b = rgb_color
        led.set(r, g, b, owner)
        

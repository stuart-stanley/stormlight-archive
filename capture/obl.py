import uuid
import time
import random
from collections import deque

class ArduindoThingy(object):
    def __init__(self, dev='/dev/ttyATH0', baud=115200):
        import serial
        self.__ser = serial.Serial(dev, baud)
        self.__init_cmd()

    def __init_cmd(self):
        cookie = str(uuid.uuid4())
        self.__cmd_transaction(b'I', cookie, cookie)

    def __send_msg(self, cmd, payload):
        self.__ser.write(b'\1')
        self.__ser.write(cmd)
        self.__ser.write(payload)
        self.__ser.write(b'\2')
        print "SENT", cmd, payload

    def __cmd_transaction(self, cmd, payload, wait_for=None):
        self.__send_msg(cmd, payload)
        done = False
        while not done:
            print "going to wait"
            rline = self.__ser.readline().strip()
            if len(rline) == 0:
                print 'timeout'
            elif rline[0] == 'L':
                print "LOG: ", rline[1:]
            elif wait_for is not None and rline == wait_for:
                print 'got-waitfor', wait_for
                done = True
            elif rline[0] == cmd:
                if wait_for is not None:
                    if rline[1:] == wait_for:
                        print 'got-wait-for', wait_for
                        done = True
                    else:
                        print 'skip not wait-for {0} != response {1}'.format(wait_for, rline[1:])
                else:
                    print 'got-response'
                    done = True
            else:
                print 'unexpected response {0} to cmd {1}'.format(rline, cmd)
        
    def led_cmd(self, led_list, activate=True):
        led_str = ''
        for led in led_list:
            led_str = led_str + led.to_cmd_str()
        if activate:
            cmd = 'S'
        else:
            cmd = 's'
        self.__cmd_transaction( cmd, led_str)

class FakeArduindoThingy(object):
    _RADIUS = 5
    _UP_STROKE = 38
    _CROSS_STROKE = 64
    def __init__(self, strands, lights_per):
        import graphics
        self.__width = 1344
        self.__height = 840
        self.__win = GraphWin("Stormlight", self.__width, self.__height)
        border = self._RADIUS * 2
        avail_height = self.__height
        avail_width = self.__width
        self.__strands = []
        for strand in xrange(0, strands):
            a_strand = self.__make_strand(border, avail_width, avail_height)
            self.__strands.append(a_strand)
            avail_width -= self._RADIUS * 3
            avail_height -= self._RADIUS * 3

    def __make_strand(self, border, avail_width, avail_height):
        x = ((self.__width - self.__avail_width) / 2) + border
        y = self.__height - border
        rl = []
        y_space_needed = (self._RADIUS * 2) * self._UP_STROKE
        step_y = avail_height / (y_space_needed)
        assert step_y > self._RADIUS * 2, 'oops {0} not > {1}'.format(step_y, y_space_needed)
        for l in range(0, self._UP_STROKE):
            pt = graphics.Point(x, y)
            cir = graphics.Circle(pt, self._RADIUS)
            rl.append(cir)
            y = y - step_y
        x_space_needed = (self._RADIUS * 2) * (self._CROSS_STROKE - self._UP_STROKE)
        step_x = avail_width / (x_space_needed)
        for l2 in range(self._UP_STROKE, self._CROSS_STROKE):
            pt = graphics.Point(x, y)
            cir = graphics.Circle(pt, self._RADIUS)
            rl.append(cir)
            x = x + step_x
        
    def led_cmd(self, led_list, activate=True):
        for led in led_list:
            r, g, b  = led.get()
            color = graphics.color_rgb(r, g, b)

            
            led_str = led_str + led.to_cmd_str()
        if activate:
            cmd = 'S'
        else:
            cmd = 's'
        self.__cmd_transaction( cmd, led_str)


class LED(object):
    def __init__(self, strand, number):
        self.__strand = strand
        self.__number = number
        self.__r = 0
        self.__g = 0
        self.__b = 0

    def random(self, dim=1.0):
        r = int(random.randint(0,128) * dim)
        g = int(random.randint(0,255) * dim)
        b = int(random.randint(0,255) * dim)
        self.set(r, g, b)

    def set(self, r, g, b):
        self.__r = r
        self.__g = g
        self.__b = b

    def get(self):
        return self.__r, self.__g, self.__b

    def to_cmd_str(self):
        rs = '{0:01x}{1:02x}{2:02x}{3:02x}{4:02x}'.format(
            self.__strand, self.__number, self.__r, self.__g, self.__b)
        return rs

class Stormlight(object):
    def __init__(self, strands=2, lights_per=100, fake=False):
        self.__strands = {}
        for strand in xrange(0, strands):
            self.__strands[strand] = []
            for led in xrange(0,lights_per):
                l = LED(strand, led)
                l.set(led, led, led)
                self.__strands[strand].append(l)
                
        if fake:
            self.__ard = FakeArduindoThingy(strands, lights_per)
        else:
            self.__ard = ArduindoThingy()
        
    def random_all(self, dim=1.0):
        for strand in self.__strands.values():
            for led in strand:
                led.random(dim)
            self.__ard.led_cmd(strand)

    def __rnd_rgb(self, min_val, max_val):
        r = random.randint(min_val, max_val)
        g = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        return r,g,b

    def random_gradiant(self):
        f = 4
        for strand in self.__strands.values():
            r, g, b = self.__rnd_rgb(0, 255-(len(strand)*(f/2)))
            for x in xrange(0, len(strand)/2):
                led1 = strand[x]
                led1.set(r,g,b)
                led2 = strand[(x+1) * -1]
                led2.set(r,g,b)
                r += f
                g += f
                b += f
            self.__ard.led_cmd(strand)

    def boing(self):
        f = 1
        depth = 15
        trail = deque()
        for l in range(0, depth):
            trail.appendleft(l)
        r, g, b = self.__rnd_rgb(0, 255/f)
        sr = r
        sg = g
        sb = b
        for linx in xrange(depth, 100):
            tail = trail.pop()
            trail.appendleft(linx)
            for strand in self.__strands.values():
                led1 = strand[linx]
                led1.set(r,g,b)
                led2 = strand[99-linx]
                led2.set(r,g,b)
                led1 = strand[tail]
                led1.set(0,0,0)
                led2 = strand[99-tail]
                led2.set(0,0,0)
                for l in trail:
                    r = r / 2
                    g = g / 2
                    b = b / 2
                    led1 = strand[l]
                    led1.set(r,g,b)
                    led2 = strand[99-l]
                    led2.set(r,g,b)
                self.__ard.led_cmd(strand)
                r = sr
                g = sg
                b = sb

    def all_to(self, r, g, b):
        for strand in self.__strands.values():
            for linx in xrange(0,100):
                strand[linx].set(r,g,b)
            self.__ard.led_cmd(strand)

    def set(self, strand, pixel, r, g, b):
        led = self.__strands[strand][pixle]
        led.set(r,g,b)

    def update(self):
        for strand in self.__strands.values():
            self.__ard.led_cmd(strand)

            
if __name__ == '__main__':
    pl = []
    for led in xrange(0,100):
        for strand in xrange(0,2):
            l = LED(strand, led)
            #l.set(led, led, led)
            if led > 63:
                l.set(0,0,255)
            elif led > 37:
                l.set(0,0,0)
            else:
                l.set(255, 255, 255)
            pl.append(l)

    ard = ArduindoThingy()
    ard.led_cmd(pl)
    #while True:
    #    ard.led_cmd(pl)
    #    for led in pl:
    #        led.random(dim=.15)

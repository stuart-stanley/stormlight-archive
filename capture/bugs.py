import random
from collections import deque

class _PixelState(object):
    def __init__(self, r, g, b, x, strand):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__strand = strand
        self.__x = x

class Bug(object):
    MAXLEN = 10
    def __init__(self, stormlight):
        self.__stormlight = stormlight
        self.__speed = random.randint(1,10)
        self.__length = random.randint(1,self.MAXLEN)
        sr = r = self.__r = int(random.randint(0,255)*dim)
        sg = g = self.__g = int(random.randint(0,255)*dim)
        sb = b = self.__b = int(random.randint(0,255)*dim)
        self.__strand = random.randint(0,1)
        if random.randint(0,1) == 0:
            self.__direction = -1
        else:
            self.__direction = 1
        self.__x = random.randint(self.MAXLEN, 99 - self.MAXLEN)
        self.__history = deque()
        x = self.__x
        for x_off in xrange(0, self.__length + 1):
            pixel = _PixelState(r, g, b, self.__strand, x)
            self.__history.appendleft(pixel)
            x = x + self.__direction
            r = r - (sr / self.__length)
            g = g - (sg / self.__length)
            b = b - (sb / self.__length)

        


    
                            

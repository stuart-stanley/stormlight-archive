#!/usr/bin/env python
import argparse
from arrangements import HopArch
from algos import FireFlyGroup, TestFly

class _StormlightParser(object):
    def __init__(self):
        p = argparse.ArgumentParser(description='todo: fill in')
        p.add_argument('--fake', action='store_true',
                       help='run with local graphics display')

        self.__args = p.parse_args()
        self.__parser = p

    def run(self):
        if self.__args.fake:
            from displays import graphics_based_displays
            self.__display = graphics_based_displays.GraphicsDisplay()
        else:
            from displays import arduino_based_displays
            self.__display = arduino_based_displays.ArduinoDisplay()

        self.__hop_arch = HopArch(self.__display, strand_count=2)
        ffg = FireFlyGroup(self.__display, 10)
        #ffg = TestFly(self.__display)
        self.__display.lock()
        self.__display.clearall()
        self.__display.run(ffg.tick_cb)


if __name__ == '__main__':
    stl = _StormlightParser()
    stl.run()

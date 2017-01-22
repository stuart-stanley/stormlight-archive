#!/usr/bin/env python
import argparse
from arrangements import HopArch
from algos import FireFlyGroup, TestFly
from displays import arduino_based_displays

class _DisplaysProbe(object):
    def __init__(self):
        available = {}
        try:
            from displays import graphics_based_displays
            available['sim'] = graphics_based_displays.GraphicsDisplay
        except ImportError:
            pass

        try:
            from displays import raspberry_neopixel_displays
            available['pi'] = raspberry_neopixel_displays.RaspberryNeopixelDisplay
        except ImportError:
            pass

        try:
            # todo: probe for if this is really a dragino device!
            # todo: change name from arduino to dragino
            from displays import arduino_based_displays
            available['dragon'] = arduino_based_displays.ArduinoDisplay
        except ImportError:
            pass

        assert len(available) > 0, \
            'Unable to find any usable display managers'

        self.__available = available

    @property
    def choices(self):
        return self.__available.keys()

    @property
    def best_default(self):
        pref_order = ['sim', 'pi', 'dragon']
        for name in pref_order:
            if name in self.__available:
                return name
        assert False, 'impossible code path'


    def control_class(self, display_name):
        cc = self.__available[display_name]
        return cc


class _StormlightParser(object):
    def __init__(self):
        self.__display_ctl = _DisplaysProbe()

        p = argparse.ArgumentParser(description='todo: fill in')
        p.add_argument('--display', choices=self.__display_ctl.choices,
                       default=self.__display_ctl.best_default,
                       help='choose backing display type')
        p.add_argument('--use-db', dest='use_db',
                       help='run in db-driven mode')

        self.__args = p.parse_args()
        self.__parser = p

    def run(self):
        self.__display = self.__display_ctl.control_class(self.__args.display)()
        self.__hop_arch = HopArch(self.__display, strand_count=2)

        ffg = FireFlyGroup(self.__display, 30)
        #ffg = TestFly(self.__display)
        self.__display.lock()
        self.__display.clearall()
        self.__display.run(ffg.tick_cb)


if __name__ == '__main__':
    stl = _StormlightParser()
    stl.run()

#!/usr/bin/env python
import argparse
from arrangements import HopArch
from algos import (
    FireFlyGroup, TestFly,
    Flames,
    TreeCircleGroup, TestTreeCircle,
    Twinkle
)
import random


class _DisplaysProbe(object):
    def __init__(self):
        available = {}
        try:
            from displays import graphics_based_displays
            available['sim'] = graphics_based_displays.GraphicsDisplay
            print("Found display-simulator")
        except ImportError:
            print("No display-simulator")
            pass

        try:
            from displays import wled_neopixel_displays
            available['wled'] = wled_neopixel_displays.WledNeopixelDisplay
            print("Found wled display")
        except ImportError as ex:
            print("No wled display", ex)
            raise
            pass

        assert len(available) > 0, \
            'Unable to find any usable display managers'

        self.__available = available

    @property
    def choices(self):
        return self.__available.keys()

    @property
    def best_default(self):
        pref_order = ['sim', 'wled']
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
        duration = random.randint(1000, 5000)

        algo_set = [
            [Twinkle, (self.__display, 100, duration)],
            [Twinkle, (self.__display, 100, duration)],
            [FireFlyGroup, (self.__display, random.randint(2, 50), duration)],
            [FireFlyGroup, (self.__display, 2, duration)],
            [Flames, (self.__display, random.randint(50, 100), duration)],
            [Flames, (self.__display, random.randint(25, 100), duration)]
        ]

        random_algo = True
        if random_algo:
            algo_class, algo_args = algo_set[random.randint(0, len(algo_set)-1)]
            print("picked", algo_class, algo_args)
            algo_ins = algo_class(*algo_args)
        else:
            if False:
                algo_ins = TreeCircleGroup(self.__display)
                algo_ins = FireFlyGroup(self.__display, 30, duration)
                algo_ins = Flames(self.__display, 100, duration)
                algo_ins = TestFly(self.__display)
            algo_ins = TestTreeCircle(self.__display)
            algo_ins = Twinkle(self.__display, 100, duration*100)
        self.__display.lock()
        self.__display.clearall()
        self.__display.run(algo_ins.tick_cb)


if __name__ == '__main__':
    stl = _StormlightParser()
    stl.run()

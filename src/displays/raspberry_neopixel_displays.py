from .display_base import DisplayDriver, LEDThing
from neopixel import *
import time

class _WatchdogPoker(object):
    def __init__(self, wd_file='/run/stormlight-watchdog', interval=10):
        self.__wd_file = wd_file
        self.__interval = interval
        self.__last_time = None
        self.__ticks = 0
        self.__update_file()

    def __update_file(self):
        self.__last_time = time.time()
        with open(self.__wd_file, 'w') as wd_file:
            wd_file.write('last-time={0}, ticks={1}\n'.format(self.__last_time, self.__ticks))

    def handle_tick(self):
        self.__ticks += 1
        if time.time() - self.__last_time > self.__interval:
            self.__update_file()


class RaspberryNeopixelDisplay(DisplayDriver):
    _LED1_COUNT      = 100     # Number of LED pixels.
    _LED1_PIN        = 19      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
    _LED1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    _LED1_DMA        = 5       # DMA channel to use for generating signal (Between 1 and 14)
    _LED1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    _LED1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    _LED1_CHANNEL    = 1       # 0 or 1
    _LED1_STRIP      = ws.WS2811_STRIP_GRB

    _LED2_COUNT      = 100      # Number of LED pixels.
    _LED2_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
    _LED2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    _LED2_DMA        = 5      # DMA channel to use for generating signal (Between 1 and 14)
    _LED2_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    _LED2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    _LED2_CHANNEL    = 0       # 0 or 1
    _LED2_STRIP      = ws.WS2811_STRIP_GRB
    def __init__(self):
        s1 = Adafruit_NeoPixel(self._LED1_COUNT,
                               self._LED1_PIN,
                               self._LED1_FREQ_HZ,
                               self._LED1_DMA,
                               self._LED1_INVERT,
                               self._LED1_BRIGHTNESS,
                               self._LED1_CHANNEL)
        s2 = Adafruit_NeoPixel(self._LED2_COUNT,
                               self._LED2_PIN,
                               self._LED2_FREQ_HZ,
                               self._LED2_DMA,
                               self._LED2_INVERT,
                               self._LED2_BRIGHTNESS,
                               self._LED2_CHANNEL)
        s1.begin()
        s2.begin()
        for i in range(0, self._LED1_COUNT):
            s1.setPixelColor(i, Color(0, 0, 0))
        s1.show()
        #time.sleep(1)
        for i in range(0, self._LED2_COUNT):
            s2.setPixelColor(i, Color(0, 0, 0))
        s2.show()
        self.__strands = [s1, s2]
        self.__watch_dog_file = _WatchdogPoker()
        super(RaspberryNeopixelDisplay, self).__init__()

    def _led_display_context(self, led):
        assert isinstance(led, LEDThing), \
            '{0} must be an LEDThing'.format(led)
        return led

    def _start_update(self):
        self.__update_list = []

    def _add_set_to_update(self, led):
        self.__update_list.append((led, (led.red, led.green, led.blue)))
        
    def _complete_update(self):
        led_str = ''
        if len(self.__update_list) == 0:
            return

        for led, color in self.__update_list:
            gx, gy, gz = led.get_grid()
            r, g, b = color
            self.__strands[gz].setPixelColor(gx, Color(r, b, g))
        for strand in self.__strands:
            strand.show()
                                 

    def run(self, algo_tick_callback):
        while True:
            algo_tick_callback()
            self.__watch_dog_file.handle_tick()
            #time.sleep(0.1)


# todo: make ABC for strand API

class ArchStrand(object):
    def __init__(self, display, count_up, count_across, count_down, led0_pos):
        self.__display = display
        self.__count = count_up + count_across + count_down
        assert len(led0_pos) == 3, \
            'led0_pos should be x, y, z, not {0}'.format(led0_pos)

        x, y, z = led0_pos
        # XXX aspect ratio and screen size!
        step_y = 20
        step_x = 20
        leds = []
        self.__display_strand = display.add_strand()
        for _ in range(0, count_up):
            led = self.__display_strand.add_led((x, y, z))
            leds.append(led)
            y = y + step_y
        for _ in range(0, count_across):
            led = self.__display_strand.add_led((x, y, z))
            leds.append(led)
            x = x + step_x
        for _ in range(0, count_down):
            led = self.__display_strand.add_led((x, y, z))
            leds.append(led)
            y = y - step_y

        self.__leds = leds

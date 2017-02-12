from .display_base import DisplayDriver, LEDThing
import uuid


class ArduinoDisplay(DisplayDriver):
    def __init__(self, dev='/dev/ttyATH0', baud=115200):
        import serial
        self.__ser = serial.Serial(dev, baud)
        self.__init_cmd()
        super(ArduinoDisplay, self).__init__()

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
                        print 'skip not wait-for {0} != response {1}'.format(wait_or, rline[1:])
                else:
                    print 'got-response'
                    done = True
            else:
                print 'unexpected response {0} to cmd {1}'.format(rline, cmd)


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
            ls = '{0:01x}{1:02x}{2:02x}{3:02x}{4:02x}'.format(gz, gx, r, g, b)
            led_str += ls
        self.__cmd_transaction('S', led_str)

    def run(self, algo_tick_callback):
        while True:
            algo_tick_callback()


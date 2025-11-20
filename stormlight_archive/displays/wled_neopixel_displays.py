from .display_base import DisplayDriver, LEDThing
import numpy as np
import socket
import struct
import time


class WledNeopixelDisplay(DisplayDriver):
    _DDP_DATATYPE = 0x0b   # RGB (type=001), 8-bit (size=011)
    _DDP_PUSH = 0x01
    _DDP_VERSION_1 = 0x40  # version = 1
    _MAX_PIXEL_PER_PACKET = 480
    _PIXEL_DATA_PER_PACKET = _MAX_PIXEL_PER_PACKET * 3

    def __init__(self):
        self.__destination = "localhost"
        self.__destination = "glabooh.local"
        self.__dport = 4048
        s1 = 100
        s2 = 100
        self.__strand_offsets = [0, s1]
        self.__len = s1 + s2
        self.__data = np.zeros(self.__len * 3)   # *3 for RGB
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__update_count = 0
        self.__destination_id = 1
        super().__init__()
        self.__changed = True
        self._complete_update()

    def _led_display_context(self, led):
        assert isinstance(led, LEDThing), \
            '{0} must be an LEDThing'.format(led)
        return led

    def _start_update(self):
        self.__changed = False

    def _add_set_to_update(self, led):
        self.__changed = True
        gx, gy, gz = led.get_grid()
        dinx = (self.__strand_offsets[gz] + gx) * 3   # *3 for RGB
        self.__data[dinx] = led.red
        self.__data[dinx+1] = led.green
        self.__data[dinx+2] = led.blue

    def _complete_update(self):
        if not self.__changed:
            return

        self.__update_count += 1
        sequence = self.__update_count % 15 + 1
        self.__changed = False
        # make a nice flat view to send from
        byte_data = memoryview(self.__data.astype(np.uint8).ravel())
        pcnt, extra = divmod(len(byte_data), self._PIXEL_DATA_PER_PACKET)
        if extra == 0:
            pcnt -= 1

        for pinx in range(pcnt + 1):
            data_start = pinx * self._PIXEL_DATA_PER_PACKET
            data_end = data_start + self._PIXEL_DATA_PER_PACKET
            self.__send_update_part(sequence, pinx, byte_data[data_start:data_end], pinx == pcnt)

    def __send_update_part(self, sequence, packet_in_update, data, last_in_update):
        bytes_length = len(data)
        flags = self._DDP_VERSION_1
        if last_in_update:
            flags |= self._DDP_PUSH

        header = struct.pack(
            "!BBBBLH",
            flags,
            sequence,
            self._DDP_DATATYPE,
            self.__destination_id,
            packet_in_update * self._PIXEL_DATA_PER_PACKET,
            bytes_length
        )
        udp_data = header + bytes(data)
        self.__socket.sendto(udp_data, (self.__destination, self.__dport))

    def run(self, algo_tick_callback):
        while True:
            algo_tick_callback()
            time.sleep(0.005)

# The MIT License (MIT)
#
# Copyright (c) 2020 Stefan Rothe
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
ANALOG_PIN_MAP = [
    SENSOR_FLEX_INDEX_FINGER,
    SENSOR_FLEX_MIDDLE_FINGER,
    SENSOR_FLEX_RING_FINGER,
    SENSOR_FLEX_LITTLE_FINGER
]

DIGITAL_PIN_BUTTON = [
    true, true, true, true, true, true, true, true,
    false, false, false, false, true, true, true, true
]

DIGITAL_PIN_MAP = [
    BUTTON_THUMB_1,
    BUTTON_THUMB_2,
    BUTTON_THUMB_3,
    BUTTON_THUMB_4,
    BUTTON_INDEX_FINGER_1,
    BUTTON_MIDDLE_FINGER_1,
    BUTTON_RING_FINGER_1,
    BUTTON_LITTLE_FINGER_1,
    GESTURE_WAVE_LEFT,
    GESTURE_WAVE_RIGHT,
    GESTURE_WAVE_UP,
    GESTURE_WAVE_DOWN,
    BUTTON_INDEX_FINGER_2,
    BUTTON_MIDDLE_FINGER_2,
    BUTTON_RING_FINGER_2,
    BUTTON_LITTLE_FINGER_2
]
"""

class JunxionAdapter:
    def __init__(self, device):
        self.analog_pin_count = 4
        self.digital_pin_count = 8
        self.own_pin_count = 0
        self.device = device


    def board_id(self):
        return self.device.board_id


    def analog_pin_available(self, pin):
        return bool(self.device.fingers[pin].flex_sensor)


    def analog_pin_value(self, pin):
        return self.device.fingers[pin].flex_sensor.value


    def digital_pin_available(self, pin):
        return 0 <= pin < 8


    def digital_pin_active(self, pin):
        if 0 <= pin < 4:
            return self.device.button[pin].pressed
        elif 4 <= pin < 8:
            return self.device.fingers[pin - 4].button_pressed
        else:
            return False


    def own_pin_available(self, pin):
        return False


    def own_pin_value(self, pin):
        return None


class Junxion:
    def __init__(self, device):
        self.device = device
        self._data_enabled = False
        self.header_received = False
        self.package_size = 0


    def update(self):
        if not self.header_received and self.uart.in_waiting >= 3:
            header = self.uart.read(3)
            if header[0] == 0xFF and header[1] == 0xFF:
                self.header_received = True
                self.package_size = header[2]
        if self.header_received and self.uart.in_waiting > self.package_size:
            command = self.uart.read(1)
            self.handle_command(command)
            self.header_received = False
        if self._data_enabled:
            self.send_data()


    def handle_command(self, command):
        if command == 'D':
            self._data_enabled = True
        elif command == 'S':
            self._data_enabled = False
        elif command == 'B':
            self.send_board_id()
        elif command == 'J':
            self.send_junxion_id()
        elif command == 'I':
            self.send_input_config()


    def send_data(self):
        device = self.device
        data = []
        state = 0
        pos = 0
        # collect digital pin states
        for i in range(device.digital_pin_count):
            if device.digital_pin_available(i):
                if device.digital_pin_active(i):
                    state = state | (1 << pos)
                ++pos
                if pos >= 16:
                    data.append(state / 256)
                    data.append(state % 256)
                    state = 0
                    pos = 0
        if pos > 0:
            data.append(state / 256)
            data.append(state % 256)
        # collect analog pin states
        for i in range(device.analog_pin_count):
            if device.analog_pin_available(i):
                value = device.analog_pin_value(i)
                data.append(value / 256)
                data.append(value % 256)
        # collect own pin states                
        for i in range(device.own_pin_count):
            if device.own_pin_available(i):
                value = device.own_pin_value(i)
                data.append(value / 256)
                data.append(value % 256)
        self._send('d', data)


    def send_input_config():
        device = self.device
        data = []
        for i in range(device.digital_pin_count):
            if device.digital_pin_available(i):
                data.append(ord('d')) # type
                data.append(i) # id
                data.append(1) # resolution
        for i in range(device.analog_pin_count):
            if device.analog_pin_available(i):
                data.append(ord('a')) # type
                data.append(i) # id
                data.append(16) # resolution
        for i in range(device.own_pin_count):
            if device.own_pin_available(i):
                data.append(ord('o')) # type
                data.append(i) # id
                data.append(16) # resolution
        self._send('p', data)


    def send_board_id(self):
        self._send_('b', 1, [self.device.board_id()])


    def send_junxion_id(self):
        self._send('j', [1, 52])


    def _send_uint_16(self, data):
        self.uart.write(bytes([data / 256, data % 256]))


    def _send(self, command, data):
        d = [0xFF, 0xFF, len(data), ord(command)] + data
        print(d)
#        self.uart.write(bytes(d))


def test():
    j = Junxion(None)
    j.send_junxion_id()


test()
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

import flex
import board
import pca9557
import time
import neopixel

NEOPIXEL_COUNT = 20
NEOPIXEL_BRIGHTNESS = 0.2

class Finger:
    def __init__(self, i2c, flex_address, button_mask, neopixel_pin):
        try:
            self.flex = flex.Flex(i2c, flex_address)
        except:
            print("No flex sensor at", flex_address, "detected")
            self.flex = None
        self.button_mask = button_mask
        self.button_pressed = False
        self.flex_value = 0
        self.neopixel = neopixel.NeoPixel(
            neopixel_pin, NEOPIXEL_COUNT, brightness=NEOPIXEL_BRIGHTNESS, auto_write=False
        )


    def update(self, button_state):
        self.button_pressed = button_state & self.button_mask
        if self.flex:
            self.flex.poll()
            self.flex_value = self.flex.read_sample()
            self.flex.stop()
        if self.flex_value:
            self.update_neopixel()


    def update_neopixel(self):
        k = NEOPIXEL_COUNT * abs(self.flex_value) / 120
        print(self.flex_value, k)
        for i in range(NEOPIXEL_COUNT):
            self.neopixel[i] = (0, 0, 0) if k < i else (255, 0, 0)
        self.neopixel.show()


class Fingers:
    def __init__(self, i2c):
        self.index = Finger(i2c, 0x12, 0x1, board.A0)
        self.middle = Finger(i2c, 0x13, 0x2, board.A1)
        self.ring = Finger(i2c, 0x14, 0x4, board.A2)
        self.little = Finger(i2c, 0x15, 0x8, board.A3)
        self.fingers = [self.index, self.middle, self.ring, self.little]
        self.buttons = pca9557.PCA9557(i2c, 0x19)
        self.buttons.write_config(0xF0)
        self.buttons.write_polarity(0xF0)


    def __getitem__(self, index):
        return self.fingers[index]


    def update(self):
        state = (self.buttons.read_input() & 0xF0) >> 4
        self.buttons.write_output(0xFF - state)
        self.index.update(state)
#        for finger in self.fingers:
#            finger.update(state)


i2c = board.I2C()
fingers = Fingers(i2c)

while True:
    fingers.update()
    time.sleep(0.001)

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

from adafruit_bus_device.i2c_device import I2CDevice

REGISTER_INPUT    = 0x00
REGISTER_OUTPUT   = 0x01
REGISTER_POLARITY = 0x02
REGISTER_CONFIG   = 0x03

class PCA9557:
    def __init__(self, i2c, address=None):
        self.i2c_device = I2CDevice(i2c, address)
        self.buf = bytearray(2)

    def read_input(self):
        with self.i2c_device as i2c:
            i2c.write_then_readinto(bytearray([REGISTER_INPUT]), self.buf, in_end=1)
        return self.buf[0]

    def write_config(self, config):
        self.buf[0] = REGISTER_CONFIG
        self.buf[1] = config
        with self.i2c_device as i2c:
            i2c.write(self.buf)

    def write_output(self, output):
        self.buf[0] = REGISTER_OUTPUT
        self.buf[1] = output
        with self.i2c_device as i2c:
            i2c.write(self.buf)
        
    def write_polarity(self, polarity):
        self.buf[0] = REGISTER_POLARITY
        self.buf[1] = polarity
        with self.i2c_device as i2c:
            i2c.write(self.buf)

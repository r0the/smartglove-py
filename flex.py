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
`flex` - Bend Labs Soft Flex sensor device driver

Currently only supports one-axis sensor
"""

from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const
import board
import time

ADS_1_HZ = const(16384)
ADS_10_HZ = const(1638)
ADS_20_HZ = const(819)
ADS_50_HZ = const(327)
ADS_100_HZ = const(163)
ADS_200_HZ = const(81)
ADS_333_HZ = const(49)
ADS_500_HZ = const(32)

class Flex:
    def __init__(self, i2c, address=0x12):
        self.i2c_device = I2CDevice(i2c, address)
        self.buf = bytearray(3)
        self.reset()
        # Wait for device to  be reset
        time.sleep(0.05)
        self.axes = self._read_device_type()
        if self.axes != 1:
            raise RuntimeError("Invalid device type.")
        self.set_sample_rate(ADS_10_HZ)


    def read_sample(self):
        with self.i2c_device as i2c:
            i2c.readinto(self.buf, end=len(self.buf))
        if self.buf[0] == 0:
            self.sample = self._parse_int_16(self.buf[1:]) / 64.0
            return self.sample


    def poll(self):
        self._set_poll_mode(True)


    def reset(self):
        self.buf[0] = 2
        with self.i2c_device as i2c:
            i2c.write(self.buf)


    def stop(self):
        if self.polling:
            self._set_poll_mode(False)


    def set_address(self, address):
        self.buf[0] = 4
        self.buf[1] = address
        with self.i2c_device as i2c:
            i2c.write(self.buf)
        self.device_address = address


    def set_sample_rate(self, sps):
        self.buf[0] = 1
        self.buf[1] = sps & 0x00FF
        self.buf[2] = (sps & 0xFF00) >> 8
        with self.i2c_device as i2c:
            i2c.write(self.buf)


    def _parse_int_16(self, buf):
        value = buf[0] + (buf[1] << 8)
        if buf[1] & 0x80:
            value -= 0xFFFF
        return value


    def _read_device_type(self):
        with self.i2c_device as i2c:
            i2c.write_then_readinto(bytearray([10]), self.buf, in_end=len(self.buf))
        if self.buf[0] == 2:
            return self.buf[1]
        else:
            return None


    def _set_poll_mode(self, enable):
        self.buf[0] = 5
        self.buf[1] = 1 if enable else 0
        with self.i2c_device as i2c:
            i2c.write(self.buf)
        self.polling = enable

# The MIT License (MIT)
#
# Copyright (c) 2017 Radomir Dopieralski for Adafruit Industries.
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
``adafruit_bno055`` - Adafruit 9-DOF Absolute Orientation IMU Fusion Breakout - BNO055
=======================================================================================

This is a CircuitPython driver for the Bosch BNO055 nine degree of freedom
inertial measurement unit module with sensor fusion.

* Author(s): Radomir Dopieralski
"""
import time
import struct

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import Struct, UnaryStruct

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BNO055.git"

_CHIP_ID = const(0xA0)

CONFIG_MODE = const(0x00)
ACCONLY_MODE = const(0x01)
MAGONLY_MODE = const(0x02)
GYRONLY_MODE = const(0x03)
ACCMAG_MODE = const(0x04)
ACCGYRO_MODE = const(0x05)
MAGGYRO_MODE = const(0x06)
AMG_MODE = const(0x07)
IMUPLUS_MODE = const(0x08)
COMPASS_MODE = const(0x09)
M4G_MODE = const(0x0A)
NDOF_FMC_OFF_MODE = const(0x0B)
NDOF_MODE = const(0x0C)

ACCEL_4G = const(0x01)  # Default
ACCEL_62_5HZ = const(0x0C)  # Default
ACCEL_NORMAL_MODE = const(0x00)  # Default. For accel_mode property

GYRO_2000_DPS = const(0x00)  # Default. For gyro_range property
GYRO_523HZ = const(0x00)  # For gyro_bandwidth property
GYRO_32HZ = const(0x38)  # Default
GYRO_NORMAL_MODE = const(0x00)  # Default. For gyro_mode property

MAGNET_20HZ = const(0x05)  # Default
MAGNET_REGULAR_MODE = const(0x08)  # Default
MAGNET_FORCEMODE_MODE = const(0x60)  # Default

_MODE_REGISTER = const(0x3D)
_PAGE_REGISTER = const(0x07)
_ACCEL_CONFIG_REGISTER = const(0x08)
_MAGNET_CONFIG_REGISTER = const(0x09)
_GYRO_CONFIG_0_REGISTER = const(0x0A)
_GYRO_CONFIG_1_REGISTER = const(0x0B)
_CALIBRATION_REGISTER = const(0x35)
_TRIGGER_REGISTER = const(0x3F)
_POWER_REGISTER = const(0x3E)
_ID_REGISTER = const(0x00)


class _ScaledReadOnlyStruct(Struct):  # pylint: disable=too-few-public-methods
    def __init__(self, register_address, struct_format, scale):
        super().__init__(register_address, struct_format)
        self.scale = scale

    def __get__(self, obj, objtype=None):
        result = super().__get__(obj, objtype)
        return tuple(self.scale * v for v in result)

    def __set__(self, obj, value):
        raise NotImplementedError()



class BNO055_I2C:  # pylint: disable=too-many-public-methods
    """
    Base class for the BNO055 9DOF IMU sensor.
    """

    _linear_acceleration = _ScaledReadOnlyStruct(0x28, "<hhh", 1 / 100)

    def __init__(self, i2c, address=0x28):
        self.buffer = bytearray(2)
        self.i2c_device = I2CDevice(i2c, address)
        chip_id = self._read_register(_ID_REGISTER)
        if chip_id != _CHIP_ID:
            raise RuntimeError("bad chip id (%x != %x)" % (chip_id, _CHIP_ID))
        self._write_register(_POWER_REGISTER, 0x00) # POWER_NORMAL
        self._write_register(_PAGE_REGISTER, 0x00)
        self._write_register(_TRIGGER_REGISTER, 0x00)
        self.accel_range = ACCEL_4G
        self.gyro_range = GYRO_2000_DPS
        self.magnet_rate = MAGNET_20HZ
        time.sleep(0.01)
        self.mode = NDOF_MODE
        time.sleep(0.01)

    @property
    def mode(self):
        return self._read_register(_MODE_REGISTER)

    @mode.setter
    def mode(self, new_mode):
        self._write_register(_MODE_REGISTER, CONFIG_MODE)  # Empirically necessary
        time.sleep(0.02)  # Datasheet table 3.6
        if new_mode != CONFIG_MODE:
            self._write_register(_MODE_REGISTER, new_mode)
            time.sleep(0.01)  # Table 3.6

    @property
    def calibration_status(self):
        """Tuple containing sys, gyro, accel, and mag calibration data."""
        calibration_data = self._read_register(_CALIBRATION_REGISTER)
        sys = (calibration_data >> 6) & 0x03
        gyro = (calibration_data >> 4) & 0x03
        accel = (calibration_data >> 2) & 0x03
        mag = calibration_data & 0x03
        return sys, gyro, accel, mag

    @property
    def calibrated(self):
        """Boolean indicating calibration status."""
        sys, gyro, accel, mag = self.calibration_status
        return sys == gyro == accel == mag == 0x03

    @property
    def external_crystal(self):
        """Switches the use of external crystal on or off."""
        last_mode = self.mode
        self.mode = CONFIG_MODE
        self._write_register(_PAGE_REGISTER, 0x00)
        value = self._read_register(_TRIGGER_REGISTER)
        self.mode = last_mode
        return value == 0x80

    @external_crystal.setter
    def use_external_crystal(self, value):
        last_mode = self.mode
        self.mode = CONFIG_MODE
        self._write_register(_PAGE_REGISTER, 0x00)
        self._write_register(_TRIGGER_REGISTER, 0x80 if value else 0x00)
        self.mode = last_mode
        time.sleep(0.01)

    @property
    def linear_acceleration(self):
        """Returns the linear acceleration, without gravity, in m/s.
        Returns an empty tuple of length 3 when this property has been disabled by the current mode.
        """
        if self.mode in [0x09, 0x0B, 0x0C]:
            return self._linear_acceleration
        return (None, None, None)

    def _write_register(self, register, value):
        self.buffer[0] = register
        self.buffer[1] = value
        with self.i2c_device as i2c:
            i2c.write(self.buffer)

    def _read_register(self, register):
        self.buffer[0] = register
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        return self.buffer[1]

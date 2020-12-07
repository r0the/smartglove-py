# SmartGlove for Python
---

This is a [CiruitPython](https://circuitpython.org) port of the SmartGlove Neo software.

## Installation

1. Download CircuitPython 6.0.0 for the appropriate device:
    - [CircuitPython 6.0.0 for Feather M4 Express](https://downloads.circuitpython.org/bin/feather_m4_express/en_US/adafruit-circuitpython-feather_m4_express-en_US-6.0.0.uf2)
    - [CircuitPython 6.0.0 for ItsyBitsy M4 Express](https://downloads.circuitpython.org/bin/itsybitsy_m4_express/en_US/adafruit-circuitpython-itsybitsy_m4_express-en_US-6.0.0.uf2)

2. Tap the reset button on device **twice** to enter the bootloader. The device will mount as **FEATHERBOOT** or **ITSYBITSYBOOT** drive.
3. Copy the CircuitPython file to the **…BOOT** drive. The device will reboot automatically.
4. Now the device will be mounted as **CIRCUITPY** drive.
5. Remove all files on the **CIRCUITPY** drive.
6. Copy all files in this Repo to the **CIRCUITPY** drive.
7. Tap the reset button once to reboot.

## SmartGlove Hardware Overview

The SmartGlove features the following devices:

- Bosch BNO055 IMU
- NeoPixel stripes
- [VL52L1X distance measurement sensor](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html)
- SSD1306-based dot matrix display
- [PCA9557 I/O expansion](https://www.ti.com/product/PCA9557)
- [Bend Labs Soft Flex sensor](https://www.bendlabs.com)

## I2C Devices

| Device  | Function                  | Address |
|:------- |:------------------------- |:------- |
|         | flex sensor index finger  | `0x12`  |
|         | flex sensor middle finger | `0x13`  |
|         | flex sensor ring finger   | `0x14`  |
|         | flex sensor little finger | `0x15`  |
| PCA9557 | side buttons and LED      | `0x18`  |
| PCA9557 | tip buttons and LED       | `0x19`  |
| BNO055  | inertial measurement unit | `0x28`  |
| VL52L1X | distance measurement      | `0x29`  |
| SSD1306 | dot matrix display        | `0x3C`  |
| 24AA64  | EEPROM                    | `0x50`  |

## CircuitPython dependencies

The software depends on the following libraries from the [Adafruit CiruitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle):

- [libraries/helpers/bus_device](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice)
- [libraries/helpers/display_text](https://github.com/adafruit/Adafruit_CircuitPython_Display_Text)
- [libraries/drivers/bno055](https://github.com/adafruit/Adafruit_CircuitPython_BNO055)
- [libraries/drivers/displayio_ssd1306](https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SSD1306)
- [libraries/drivers/neopixel](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel)
- [libraries/drivers/ssd1306](https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SSD1306)

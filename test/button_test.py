import pca9557
import board
import time

I2C_SIDE_BUTTONS_ADDRESS = 0x18

i2c = board.I2C()

side_buttons = pca9557.PCA9557(i2c, I2C_SIDE_BUTTONS_ADDRESS)
side_buttons.write_config(0xF0)
side_buttons.write_polarity(0xF0)

def read_buttons():
    result = 0
    buttons = side_buttons.read_input() & 0xF0
    print(buttons)
    side_buttons.write_output((0xFF - buttons) >> 4)
    return result

while True:
    read_buttons()

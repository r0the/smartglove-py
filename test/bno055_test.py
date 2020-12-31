import time
import board
import busio
import adafruit_bno055

# Use these lines for I2C
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# User these lines for UART
# uart = busio.UART(board.TX, board.RX)
# sensor = adafruit_bno055.BNO055_UART(uart)

while True:
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print()

    time.sleep(1)
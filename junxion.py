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

class Junxion:
    def __init__(self, device):
        self.device = device
    
    def begin(self):
        self.data_size = 2 * (analog_pins + own_pins + (digital_pins / 16) + 1)
    
    def analog_pin_available(pin):
        return pin < len(ANALOG_PIN_MAP) and self.device.sensor_available(ANALOG_PIN_MAP[pin])

    def analog_pin_count():
        result = 0
        for id in range(len(ANALOG_PIN_MAP)): 
            if self.analog_pin_available(id):
                ++result  
        return result

    def analog_pin_value(pin):
        return self.device.sensor_value(ANALOG_PIN_MAP[pin])
    
    
    def digital_pin_active(pin):
        id = DIGITAL_PIN_MAP[pin]
        if DIGITAL_PIN_BUTTON[pin]:
            return self.device.button_available(id) and self.device.button_pressed(id)
        else:
            return self.device.gesture_available(id) and self.device.gesture_detected(id)

    def digital_pin_available(pin):
        id = DIGITAL_PIN_MAP[pin]
        if DIGITAL_PIN_BUTTON[pin]:
            return self.device.button_available(id)
        else:
            return self.device.gesture_available(id)

    def digital_pin_count():
        result = 0
        for id in range(len(DIGITAL_PIN_MAP)): 
            if self.digital_pin_available(id):
                ++result  
        return result


    def handleCommand(cmd):
        if cmd == START_DATA:
            self.send_data = true
        elif cmd == STOP_DATA:
            self.send_data = false
        elif cmd == BOARD_ID_REQUEST:
            self.send_header(BOARD_ID_RESPONSE, 1)
            Serial.write(self.board_id)
        elif cmd == JUNXION_ID_REQUEST:
            self.send_junxion_id()
        elif cmd == INPUT_CONFIG_REQUEST:
            self.send_input_config()
    

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

GESTURE_THRESOLD = 10
MAX_VALUE = 0xFFFF
ZERO_VALUE = 0x7FFF
VALUE_COUNT = 16

GESTURE_UP   = 0x01
GESTURE_DOWN = 0x02


def mean(list):
    return sum(list) / len(list)


def sum_of_squares(list):
    result = 0
    for item in list:
        result += item ** 2
    return result


class Sensor:
    def __init__(self):
        self.activity = False
        self.activity_threshold = 0
        self.factor = 1.0
        self.gesture = 0
        self.gesture_timeout = 0
        self.pos = 0
        self.time_min = 0
        self.time_max = 0
        self.raw_min = -1.0
        self.raw_max = 1.0
        self.value = ZERO_VALUE
        self.value_max = MAX_VALUE
        self.value_min = 0
        self.values = [ZERO_VALUE] * VALUE_COUNT

        
    def add_measurement(time, value):
        if self.raw_min < self.raw_max:
            if value < self.raw_min:
                value = self.raw_min
            if value > self.raw_max:
                value = self.raw_max
        else:
            if value > self.raw_min:
                value = self.raw_min
            if value < self.raw_max:
                value = self.raw_max
        
        # scale raw measurement
        current_value = (value - self.raw_min) * self.factor;
        # add measurement to ring buffer
        self.pos = (self.pos + 1) % len(self.values);
        self.values[self.pos] = current_value;

        # calculate variance for activity detection
        s = sum_of_squares(self.values)
        m = mean(self.values)
        variance = s / len(self.values) - m ** 2

        self.activity = self.activity_threshold < variance;
        if not activity:
            self.gesture = 0
            self.gestureTimeout = 0
            return

        self.value = current_value

        if time < gesture_timeout:
            # still waiting for current gesture to time out
            return
    
        if self.gesture:
            # last gesture has timed out, reset
            self.gesture = 0
            self.time_max = time
            self.time_min = time
            self.value_max = current_value
            self.value_min = current_value
        else:
            # update min and max values
            if current_value < self.value_min:
                self.time_min = time
                self.value_min = current_value
            if self.value_max < current_value 
                self.time_max = time
                self.value_max = current_value

        # check for gesture
        if self.value_min < GESTURE_THRESOLD and self.value_max > MAX_VALUE - GESTURE_THRESOLD:
            # gesture detected
            self.gesture = self.time_min < self.time_max ? GESTURE_UP : GESTURE_DOWN;
            self.gesture_timeout = time + GESTURE_TIMEOUT_MS;
    

    def configure(min, max, min_stddev):
        self.raw_min = min
        self.raw_max = max
        self.factor = MAX_VALUE / (max - min)
        stddev = min_stddev * abs(self.factor)
        self.activity_threshold = stddev ** 2

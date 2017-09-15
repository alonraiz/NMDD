import enum
import time
import random
import logging

import gevent

from .gpio import GPIO


class LedStrip(object):
    class STATE(enum.Enum):
        OFF = 0
        RANDOM = 1
        RED_FLASH = 2
        GREEN_FLASH = 3
        BLUE_FLASH = 4

    class SPEED(enum.Enum):
        FAST = 0.3
        NORMAL = 1
        SLOW = 2

    TICK_TIME_IN_SECONDS = SPEED.NORMAL.value

    def __init__(self, red_pin, green_pin, blue_pin):
        self._state = self.STATE.OFF
        self._internal_state = None
        self._pins = [red_pin, green_pin, blue_pin]
        self._tick_size_in_seconds = self.TICK_TIME_IN_SECONDS

        for pin in self._pins:
            GPIO.setup(pin, GPIO.OUT)

        # Start the task
        gevent.spawn(self._task)

    def set_speed(self, speed):
        self._set_tick(speed.value)

    def set_state(self, state):
        self._state = state
        self._internal_state = None
        self._clear_tick()

    def _set_tick(self, tick):
        self._tick_size_in_seconds = tick

    def _clear_tick(self):
        self._tick_size_in_seconds = self.TICK_TIME_IN_SECONDS

    def _task(self):
        logging.info("LesStrip starting")
        while True:
            logging.info("LesStrip loop")
            if self._state == self.STATE.OFF:
                pass

            elif self._state == self.STATE.RANDOM:
                for pin in self._pins:
                    GPIO.output(pin, random.choice([True, False]))

            elif self._state == self.STATE.RED_FLASH:
                self._internal_state = False if self._internal_state else True
                GPIO.output(self._pins[0], self._internal_state)
                GPIO.output(self._pins[1], False)
                GPIO.output(self._pins[2], False)

            elif self._state == self.STATE.GREEN_FLASH:
                self._internal_state = False if self._internal_state else True
                GPIO.output(self._pins[0], False)
                GPIO.output(self._pins[1], self._internal_state)
                GPIO.output(self._pins[2], False)

            elif self._state == self.STATE.BLUE_FLASH:
                self._internal_state = False if self._internal_state else True
                GPIO.output(self._pins[0], False)
                GPIO.output(self._pins[1], False)
                GPIO.output(self._pins[2], self._internal_state)

            time.sleep(self.TICK_TIME_IN_SECONDS)

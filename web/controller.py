import time
import logging

from .gpio import GPIO

DRINK_ML_IN_SECOND = 3.7
DRINK_SIZE_IN_ML = 30

class ControllerManager(object):
    def __init__(self, state, pins):
        self._state = state
        self._pins = pins

        for pin in self._pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def mix(self, drink):
        self._state.current.status = "Pouring drinks"
        self._state.flush()
        time.sleep(1)

        # Cut drink
        drink = drink[:len(self._pins)]

        # Normalize values
        drink_total = sum(x[2] for x in drink)
        values_percent = [(x[0], x[1], x[2]*100/drink_total) for x in drink]
        values_ml = [(x[0], x[1], x[2]*DRINK_SIZE_IN_ML/100) for x in values_percent]

        logging.info("DRINKS %s", drink)
        logging.info("PERCENT %s", values_percent)
        logging.info("VALUES %s", values_ml)

        # Pour drinks
        for idx, value_entry in enumerate(values_ml):
            value_pin_idx, value_type, value_ml = value_entry
            value_pin = self._pins[value_pin_idx]

            # Drink state
            self._state.current.status = "Pouring drink %d [drink=%s, ml=%s, pin=%s]" % (idx+1, value_type, value_ml, value_pin)
            self._state.flush()

            logging.info("Pouring drink %d [pin=%s]", idx+1, value_pin)

            # Pour drink
            sleep_in_ms = value_ml/DRINK_ML_IN_SECOND
            GPIO.output(value_pin, True)
            logging.info("Sleeping for %s", sleep_in_ms)
            time.sleep(sleep_in_ms)
            logging.info("Finished sleeping")
            GPIO.output(value_pin, False)
            time.sleep(1)


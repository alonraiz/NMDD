import logging

try:
    import RPi.GPIO as GPIO
except ImportError:
    class GPIO(object):
        BCM = 0
        OUT = 0

        @classmethod
        def setmode(cls, mode):
            pass

        @classmethod
        def setwarnings(cls, toggle):
            pass

        @classmethod
        def setup(cls, pin, state):
            pass

        @classmethod
        def output(cls, pin, state):
            logging.debug("OUTPUT pin=%s state=%s", pin, state)

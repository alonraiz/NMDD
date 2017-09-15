import time

class ControllerManager(object):
    def __init__(self, state):
        self._state = state

    def mix(self, drink):
        # self._state.current.status = "Initializing server"
        # self._state.flush()
        # time.sleep(2)
        # self._state.current.status = "Pouring liquids"
        # self._state.flush()
        # time.sleep(3)
        self._state.current.status = "You are done!"
        self._state.flush()
        time.sleep(1)

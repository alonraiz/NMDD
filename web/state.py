import json
import logging
import contextlib

import munch

class State(object):
    def __init__(self):
        self._state = munch.Munch()
        self._handlers = set()

    @contextlib.contextmanager
    def on_notification(self, handler):
        # Register handler
        self._handlers.add(handler)

        try:
            yield
        except:
            self._handlers.remove(handler)

    def flush(self):
        for handler in self._handlers:
            try:
                handler()
            except Exception:
                logging.exception("Failed to handler notification handler")

    def serialize(self):
        return json.dumps(self._state)

    @property
    def current(self):
        return self._state

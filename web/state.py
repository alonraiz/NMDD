import json
import logging
import contextlib

class State(object):
    def __init__(self):
        self._state = {}
        self._handlers = []

    @contextlib.contextmanager
    def on_notification(self, handler):
        # Register handler
        self._handlers.append(handler)

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

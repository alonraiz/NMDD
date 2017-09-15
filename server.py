import os
import json
import logging
logging.basicConfig(level=logging.DEBUG)


import flask
import flask_sockets
import sqlalchemy

import munch

from gevent import pywsgi, monkey
from geventwebsocket.handler import WebSocketHandler

import web

# Parameters
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
WEB_PATH = os.path.join(ROOT_PATH, "web")
DATABASE_PATH = os.path.join(ROOT_PATH, "data", "nmdd.sqlite")
BASELINE_PATH = os.path.join(ROOT_PATH, "data", "nmdd.baseline")

MAPPING = {
    "White Rum": 2,
    "Vodka": 3,
    "Gin": 4,
    "Pomegranate Juice": 25,
    "Orange Juice": 8,
    "Lemon Juice": 10,
    "Apple Juice": 9,
    "Crannberry Juice": 11,
    "Coinntreau": 27,
    "Campari": 13,
    "White Dry Vermouth": 6,
    "Red Sweet Vermouth": 17,
    "Cherry liquor": 5,
    #"Something Else": 22
}

def main():
    # Monkey patch
    monkey.patch_all()

    # Initialize gpio
    web.gpio.GPIO.setmode(web.gpio.GPIO.BCM)
    web.gpio.GPIO.setwarnings(False)

    # Initialize flask app
    app = flask.Flask(__name__,
                      static_folder="web/build",
                      static_url_path="/static")
    sockets = flask_sockets.Sockets(app)

    # Configure database
    logging.debug("Using database %s", DATABASE_PATH)
    engine = sqlalchemy.create_engine("sqlite:///{}".format(DATABASE_PATH))

    if not os.path.exists(DATABASE_PATH):
        logging.info("Bootstrapping database %s", DATABASE_PATH)
        web.model.bootstrap(engine)

    # State manager
    state = web.state.State()
    state.current.view = "idle"

    # Initialize nmdd controller
    controller = web.controller.ControllerManager(state, list(MAPPING.values()))

    # Load ml baseline
    baseline = None
    if os.path.exists(BASELINE_PATH):
        baseline = web.ml.ExportedBaseline(open(BASELINE_PATH, "rt").read())

    # Initialize ml library
    ml = web.ml.MachineLearningManager(state,
                                       baseline=baseline,
                                       drinks_filter=lambda type, weight: type in MAPPING)

    # Export
    ml.export(BASELINE_PATH)

    # Led strip
    leds = web.led.LedStrip(23, 18, 24)
    leds.set_state(web.led.LedStrip.STATE.RANDOM)
    leds.set_speed(web.led.LedStrip.SPEED.SLOW)

    # Processing
    def process(action, data=None):
        logging.info("Processing action %s", action)

        if action == "DRINK":
            # Start drinking
            state.current.view = "pouring"
            state.flush()

            # Red flash
            leds.set_state(web.led.LedStrip.STATE.RED_FLASH)
            leds.set_speed(web.led.LedStrip.SPEED.FAST)

            # Get a drink from the ml
            drink_suggest = ml.suggest()
            drink_mapped = [(MAPPING[type], type, value) for type, value in drink_suggest]
            logging.info("Suggested drink %s", drink_suggest)

            # Mix the drink
            controller.mix(drink_mapped)

            # Move to feedback
            state.current.view = "feedback"
            state.flush()

            # Green flash
            leds.set_state(web.led.LedStrip.STATE.GREEN_FLASH)
            leds.set_speed(web.led.LedStrip.SPEED.FAST)

        elif action == "FEEDBACK":
            # Accept changes
            ml.accept(
                **{x.type:x.result for x in data}
            )

            # Dump baseline
            ml.export(BASELINE_PATH)

            # Move to capture
            #state.current.view = "capturing"
            state.current.view = "idle"
            state.flush()

            # Clear flash
            leds.set_state(web.led.LedStrip.STATE.RANDOM)
            leds.set_speed(web.led.LedStrip.SPEED.SLOW)

        elif action == "DONE":
            # Move to capture
            state.current.view = "idle"
            state.flush()

    # Configure main view
    @sockets.route("/realtime")
    def ws_realtime(ws):
        def on_update():
            ws.send(json.dumps(dict(state=state.current)))

        # Push initial
        on_update()

        # Wait for changes
        with state.on_notification(on_update):
            while not ws.closed:
                try:
                    raw = ws.receive()
                    if raw is None:
                        continue
                    message = munch.munchify(json.loads(raw))
                    if "action" in message:
                        process(message.action, message.data)
                except:
                    logging.exception("Failed processing message")

    @app.route("/")
    def get_index():
        return app.send_static_file("index.html")

    @app.route("/state")
    def get_state():
        return state.serialize()

    # Run server
    server = pywsgi.WSGIServer(("0.0.0.0", 5000), app,
                               handler_class=WebSocketHandler,
                               log=logging,
                               error_log=logging,
                               keyfile="ssl.key",
                               certfile="ssl.crt")
    server.serve_forever()

if "__main__" == __name__:
    main()

import os
import json
import random
import logging
logging.basicConfig(level=logging.INFO)


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


# PIN LIST 2,3,4,25,8,10,9,11,27,13,6,17,5,22
MAPPING = [
    ("White Rum", 10), ##
    ("Vodka", 2), ##
    ("Gin", 13), ##
    ("Pomegranate Juice", 11), ##
    ("Orange Juice", 4), ##
    ("Lemon Juice", 9), ##
    ("Apple Juice", 27), ## Grapefruit
    ("Crannberry Juice", 8), ##
    ("Coinntreau", 22), ##
    ("Campari", 6), ##
    ("White Dry Vermouth", 3), ##
    ("Red Sweet Vermouth", 25), ##
    ("Cherry liquor", 5), ##
    #("Something Else", 13)
]
MAPPING_PINS = [x[1] for x in MAPPING]
MAPPING_KEY_TO_INDEX = {entry[0]:idx for idx,entry in enumerate(MAPPING)}

NON_ALCOHOLIC = ["Pomegranate Juice", "Orange Juice", "Lemon Juice", "Apple Juice", "Crannberry Juice"]

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
    state.current.latest = None

    # Initialize nmdd controller
    controller = web.controller.ControllerManager(state, MAPPING_PINS)

    # Load ml baseline
    baseline = None
    if os.path.exists(BASELINE_PATH):
        baseline = web.ml.ExportedBaseline(open(BASELINE_PATH, "rt").read())

    # Initialize ml library
    ml = web.ml.MachineLearningManager(state,
                                       baseline=baseline,
                                       drinks_filter=lambda type, weight: type in MAPPING_KEY_TO_INDEX)

    # Export
    ml.export(BASELINE_PATH)

    # Led strip
    leds = web.led.LedStrip(23, 18, 24)
    leds.set_state(web.led.LedStrip.STATE.RANDOM)
    leds.set_speed(web.led.LedStrip.SPEED.SLOW)

    # Update last known
    state.current.latest = "Last Known Good %s" % (",".join("%s (%s)" % (x[0], x[1]) for x in ml.current()))

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
            if data.style == "LUCKY":
                logging.info("Fetching LUCKY drink")
                drink_suggest = ml.suggest()
            elif data.style == "PREGNANT":
                logging.info("Fetching PREGNANT drink")
                drink_suggest = [
                    (random.choice(NON_ALCOHOLIC), random.randint(0, 100))
                    for _ in range(len(NON_ALCOHOLIC))
                ]
            else:
                logging.info("Fetching BEST drink")
                drink_suggest = ml.current()

            drink_mapped = [(MAPPING_KEY_TO_INDEX[type], type, value) for type, value in drink_suggest]
            logging.info("Suggested drink %s", drink_suggest)

            # Update latest
            state.current.latest = "Last Known Good %s" % (",".join("%s (%s)" % (x[1], x[2]) for x in drink_mapped))

            # Mix the drink
            controller.mix(drink_mapped)

            # Move to feedback
            if data.style == "BEST" or data.style == "PREGNANT":
                state.current.view = "idle"
            else:
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

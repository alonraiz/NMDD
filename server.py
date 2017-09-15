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


def main():
    # Monkey patch
    monkey.patch_all()

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
    controller = web.controller.ControllerManager(state)

    # Initialize ml library
    ml = web.ml.MachineLearningManager(state)

    # Processing
    def process(action, data=None):
        logging.info("Processing action %s", action)

        if action == "DRINK":
            # Start drinking
            state.current.view = "pouring"
            state.flush()

            # Get a drink from the ml
            drink = ml.suggest()

            # Mix the drinkg
            controller.mix(drink)

            # Move to feedback
            state.current.view = "feedback"
            state.flush()

        elif action == "FEEDBACK":
            # Move to capture
            state.current.view = "capturing"
            state.flush()

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

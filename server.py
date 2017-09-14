import os
import json
import logging
logging.basicConfig(level=logging.DEBUG)


import sqlalchemy
import flask
import flask_sockets

import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

import web

# Parameters
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
WEB_PATH = os.path.join(ROOT_PATH, "web")
DATABASE_PATH = os.path.join(ROOT_PATH, "data", "nmdd.sqlite")


def main():
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

    # Initialize nmdd controller
    controller = web.controller.ControllerManager()

    # Initialize ml library
    ml = web.ml.MachineLearningManager()

    # Configure main view
    @sockets.route("/realtime")
    def ws_realtime(ws):
        def on_update():
            ws.send(json.dumps(dict(state=state.state)))

        with state.on_notification(on_update):
            while not ws.closed:
                ws.receive()

    @app.route("/")
    def get_index():
        return app.send_static_file("index.html")

    @app.route("/state")
    def get_state():
        return state.serialize()

    # Run server
    server = pywsgi.WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler, log=logging, error_log=logging)
    server.serve_forever()

if "__main__" == __name__:
    main()

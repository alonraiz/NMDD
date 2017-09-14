import os
import logging
logging.basicConfig(level=logging.DEBUG)


import sqlalchemy
import flask

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

    # Configure database
    logging.debug("Using database %s", DATABASE_PATH)
    engine = sqlalchemy.create_engine("sqlite:///{}".format(DATABASE_PATH))

    if not os.path.exists(DATABASE_PATH):
        logging.info("Bootstrapping database %s", DATABASE_PATH)
        web.model.bootstrap(engine)

    # Initialize nmdd controller
    controller = web.controller.ControllerManager()

    # Initialize ml library
    ml = web.ml.MachineLearningManager()

    # Configure main view
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    # Run server
    app.run(debug=True)

if "__main__" == __name__:
    main()

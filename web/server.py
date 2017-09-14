from flask import Flask
app = Flask(__name__, static_folder="build")

@app.route("/")
def index():
    return app.send_static_file("index.html")

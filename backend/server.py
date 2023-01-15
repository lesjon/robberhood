import sys
import json
import logging
import pathlib

import flask

from classifier import classifier

BUFFER = "received/"
pathlib.Path(BUFFER).mkdir(parents=True, exist_ok=True)

logging.getLogger().setLevel(logging.DEBUG)

logging_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging_formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

app = flask.Flask(__name__)

@app.route("/")
def get_hello_world():
    return "<p>Hello, World!</p>"


@app.route("/models")
def get_models():
    models = classifier.get_models()
    return flask.render_template("models.html", models=models)

@app.route("/statements", methods = ["GET","POST"])
def statements():
    logger.debug(f"{flask.request=}")
    logger.debug(f"{flask.request.files=}")
    match flask.request.method:
        case "POST":
            f = flask.request.files['csv']
            logger.debug(f"{f=}")
            f.save(BUFFER + f.filename)
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        case "GET":
            return ["not yet implemented"]
            

if __name__ == "__main__":
    app.run()
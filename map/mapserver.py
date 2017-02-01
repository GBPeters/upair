from flask import Flask, jsonify
from flask import url_for
from werkzeug.utils import redirect

from map.realtime import RealtimeLoader

app = Flask(__name__)

DB = "LOCAL"

@app.route("/")
def home():
    return redirect(url_for("static", filename="flightmap.html"))


@app.route("/testgjson")
def testgjson():
    geom = {"geometry": {"type": "Point", "coordinates": [51.56, 38.18]}, "type": "Feature", "properties": {}}
    gjson = jsonify(geom)
    return gjson


@app.route("/now")
def now():
    loader = RealtimeLoader(DB)
    return jsonify(loader.getGJSON())


def start(db="local", host="0.0.0.0"):
    global DB
    DB = db
    app.run(host=host)

if __name__ == "__main__":
    app.run()

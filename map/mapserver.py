"""
Flask-based mapserver
"""

from flask import Flask, jsonify
from flask import url_for
from werkzeug.utils import redirect

from map.realtime import RealtimeLoader

app = Flask('map', root_path="/root/git/upair/map/")

DB = "LOCAL"

@app.route("/")
def home():
    """
    Home directory redirects to flightmap.html
    :return:
    """
    return redirect(url_for("static", filename="flightmap.html"))


@app.route("/testgjson")
def testgjson():
    """
    Returns a testGJSON with one coordinate
    :return:
    """
    geom = {"geometry": {"type": "Point", "coordinates": [51.56, 38.18]}, "type": "Feature", "properties": {}}
    gjson = jsonify(geom)
    return gjson


@app.route("/now")
def now():
    """
    Return current positions and flightpaths
    :return:
    """
    return RealtimeLoader(DB).getNow()


# Disabled, airways too large for Leaflet too display.
# @app.route("/airways")
# def airways():
#     loader = RealtimeLoader(DB)
#     return jsonify(loader.getAirways())

def start(db="local", host="0.0.0.0"):
    global DB
    DB = db

    app.run(host=host)

if __name__ == "__main__":
    app.run()

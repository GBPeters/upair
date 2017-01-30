import webbrowser
from os import path

from flask import Flask, jsonify
from flask import url_for
from werkzeug.utils import redirect

from bot.opensky import downloadJSON, convertToGeoJSON

app = Flask(__name__)


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
    j = downloadJSON()
    dic = convertToGeoJSON(j)
    gjson = jsonify(dic)
    return gjson


if __name__ == "__main__":
    app.run()

import json

from analysis.plane import PlaneFactory
from db.pghandler import Connection


class RealtimeLoader:
    def __init__(self, db="LOCAL"):
        self.db = db

    def getGJSON(self):
        positions = self.getPositions()
        paths = self.getFlightPaths()
        return {"type": "FeatureCollection",
                "features": positions + paths}

    def getPositions(self):
        with Connection(conf=self.db) as c:
            sql = "SELECT * FROM rtstates WHERE latitude IS NOT NULL"
            states = c.selectAll(sql)
            pf = PlaneFactory()
            return [pf.buildPlaneFromSQL(s).getGJSONPlane() for s in states]

    def getFlightPaths(self):
        with Connection(conf=self.db) as c:
            sql = "SELECT icao24, callsign, minres, maxres, mintime, maxtime, ST_AsGeoJSON(geom) FROM rtflightpaths"
            paths = c.selectAll(sql)
            features = []
            for icao24, callsign, minres, maxres, mintime, maxtime, geom in paths:
                f = {"type": "Feature",
                     "geometry": json.loads(geom),
                     "properties": {
                         "id": "%s:%s" % (icao24, callsign),
                         "icao24": icao24,
                         "callsign": callsign,
                         "minres": minres,
                         "maxres": maxres,
                         "mintime": mintime,
                         "maxtime": maxtime
                     }}
                features.append(f)
            return features


if __name__ == '__main__':
    RealtimeLoader().getFlightPaths()

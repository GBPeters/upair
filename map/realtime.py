import json

from analysis.plane import PlaneFactory
from db.pghandler import Connection


class RealtimeLoader:
    def __init__(self, db="LOCAL"):
        self.db = db

    def getNow(self):
        positions = self.getPositions()
        paths = self.getFlightPaths()
        return '{"type": "FeatureCollection", ' \
               ' "features": %s,%s }' % (positions[:-1], paths[1:])

    def getPositions(self):
        with Connection(conf=self.db) as c:
            sql = "SELECT * FROM rtstates WHERE latitude IS NOT NULL"
            states = c.selectAll(sql)
            pf = PlaneFactory()
            return json.dumps([pf.buildPlaneFromSQL(s).getGJSONPlane() for s in states])

    def getFlightPaths(self):
        with Connection(conf=self.db) as c:
            sql = "SELECT icao24, callsign, ST_AsGeoJSON(geom) FROM rtflightpaths"
            paths = c.selectAll(sql)
            features = []
            for icao24, callsign, geom in paths:
                f = {"type": "Feature",
                     "geometry": json.loads(geom),
                     "properties": {
                         "id": "%s:%s" % (icao24, callsign),
                         "icao24": icao24,
                         "callsign": callsign,
                     }}
                features.append(f)
            return json.dumps(features)

    def getAirways(self):
        with Connection(conf=self.db) as c:
            sql = "SELECT ST_AsGeoJSON(geom) FROM airways LIMIT 1"
            return json.loads(c.selectOne(sql)[0])


if __name__ == '__main__':
    RealtimeLoader().getFlightPaths()

from math import copysign

from analysis.plane import PlaneFactory
from db.pghandler import Connection


class FlightPath:
    def __init__(self, plane=None, responses={}):
        self.plane = plane
        self.responses = responses

    def getCoords(self):
        coords = self.responses = [(r[2], r[1]) for r in self.responses.values()]
        # Fix dateline crossings, check for onGround=True
        mls = []
        spl = 0
        xn0, yn0 = coords[0]
        for i in range(len(coords[1:]) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            if abs(x2 - x1) > 180:
                xn1 = copysign(180, x1)
                xn2 = copysign(180, x2)
                d1 = xn1 - x1
                d2 = xn2 - x2
                yn2 = yn1 = (d1 / float(d1 + d2)) * (y2 - y1) + y1
                mls += [[(xn0, yn0)] + coords[spl:i + 1] + [(xn1, yn1)]]
                xn0, yn0 = xn2, yn2
                spl = i + 1
        return [[(xn0, yn0)] + coords[spl:]]

    def getLineWKT(self):
        mls = self.getCoords()
        mlss = "MULTILINESTRING ("
        for ls in mls:
            lss = "("
            for x, y in ls:
                lss += "%f %f," % (x, y)
            mlss += lss[:-1] + "),"
        return mlss[:-1] + ")"


class FlightPathFactory:
    def __init__(self, flightPaths=[]):
        self._flightPaths = flightPaths

    def buildFlightPathsFromSQL(self, rtstates, states):
        self._flightPaths = []
        pf = PlaneFactory()
        planes = [pf.buildPlaneFromSQL(r).plane for r in rtstates]
        planedict = dict([(p.icao, p) for p in planes])
        responsedict = dict([(p.icao, []) for p in planes])
        for icao24, callsign, response_id, postime, latitude, longitude in states:
            responsedict[icao24].append((response_id, postime, latitude, longitude))
        for icao24 in responsedict:
            cols = map(list, zip(*responsedict[icao24]))
            responses = dict([(r[0], (r[1], r[2], r[3])) for r in responsedict[icao24]])
            self._flightPaths.append(FlightPath(planedict[icao24], responses))
        return self

    def pathGenerator(self):
        for fp in self._flightPaths:
            yield fp

    def sqlInsertGenerator(self, tablename):
        for fp in self._flightPaths:
            yield "INSERT INTO %s (icao24, callsign, geom) VALUES ('%s', '%s', ST_GeomFromText('%s'))" % \
                  (tablename, fp.plane.icao, fp.plane.tailnum, fp.getLineWKT())


if __name__ == '__main__':
    with Connection(autocommit=False) as c:
        sql = 'SELECT * FROM rtstates WHERE time_position IS NOT NULL'
        rtstates = c.selectAll(sql)
        sql = '''
        WITH res AS (SELECT id FROM responses
        WHERE to_timestamp(time) > CURRENT_TIMESTAMP - INTERVAL '1 day'
        ORDER BY time ASC LIMIT 1),
        s AS (SELECT icao24, callsign, response_id, time_position, latitude, longitude
        FROM states WHERE response_id >= (SELECT * FROM res)
        AND time_position IS NOT NULL)
        SELECT s.* FROM s INNER JOIN (SELECT icao24, callsign FROM rtstates WHERE time_position IS NOT NULL)
        AS r ON s.icao24=r.icao24 AND s.callsign=r.callsign
        ORDER BY time_position DESC
        '''
        states = c.selectAll(sql)
        for sql in FlightPathFactory().buildFlightPathsFromSQL(rtstates, states).sqlInsertGenerator("rtflightpaths"):
            c.execute(sql)
        c.commit()

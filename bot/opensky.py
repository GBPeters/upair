"""
This module contains functions for downloading and storing OpenSky data
"""

# Imports
import json
import urllib2
from threading import Thread

from analysis.flightpath import FlightPathFactory
from db.pghandler import Connection

# Constants
API_URL = "https://opensky-network.org/api/states/all"
STRING_INDICES = [1,2,3]
FLOAT_INDICES = [6,7,8,10,11,12]
INT_INDICES = [0,4,5]

def downloadJSON(url=API_URL):
    """
    Download JSON from url and return loaded object
    :param url: The url to download from
    :return: The loaded JSON data (list, dictionary, etc.)
    """
    raw = urllib2.urlopen(url).read()
    return json.loads(raw)


def storeResponse(response, db="LOCAL"):
    """
    Store
    :param The response in a JSON object, as specified on opensky-network.org/apidoc/rest.web
    :return: Boolean, whether storing has succeeded.
    """
    with Connection(conf=db, autocommit=False) as con:
        sql = "INSERT INTO responses (time) VALUES (%d) RETURNING id" % response["time"]
        rid = con.selectOne(sql)[0]
        sql = "TRUNCATE TABLE rtstates"
        con.execute(sql)
        for state in response["states"]:
            values = [rid] + state[:-1]
            # Clean values
            i = 0
            strvalues = []
            for v in values:
                if v is None:
                    strvalues += ['NULL']
                else:
                    if i in STRING_INDICES:
                        strvalues += ["'%s'" % v]
                    elif i in FLOAT_INDICES:
                        strvalues += ["%f" % v]
                    elif i in INT_INDICES:
                        strvalues += ["%d" % v]
                    else:
                        strvalues += ["%s" % v]
                i += 1
            sql = "INSERT INTO rtstates " \
                  "(response_id, icao24, callsign, origin_country, time_position, time_velocity, " \
                  "longitude, latitude, altitude, on_ground, velocity, heading, vertical_rate) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " % tuple(strvalues)
            con.execute(sql)
        # Collision risk check
        sql = '''
        UPDATE rtstates r1 SET atrisk=exists(
        SELECT 1 FROM rtstates r2
        WHERE ST_DWithin(ST_MakePoint(r1.longitude, r1.latitude)::geography, ST_MakePoint(r2.longitude, r2.latitude)::geography, 8000)
        AND abs(r1.altitude - r2.altitude) < 300 AND r1.icao24 <> r2.icao24)
        '''
        con.execute(sql)
        sql = "INSERT INTO states " \
              "(response_id, icao24, callsign, origin_country, time_position, time_velocity, " \
              "longitude, latitude, altitude, on_ground, velocity, heading, vertical_rate) " \
              "SELECT response_id, icao24, callsign, origin_country, time_position, time_velocity, " \
              "longitude, latitude, altitude, on_ground, velocity, heading, vertical_rate " \
              "FROM rtstates; "
        con.execute(sql)
        con.commit()
    return True


def createFlightPaths(db="LOCAL"):
    """
    Create flightpaths from rtstates and store them in table rtflightpaths
    :param db: The db settings to use
    :return: None
    """
    with Connection(conf=db) as con:
        sql = 'SELECT * FROM rtstates WHERE time_position IS NOT NULL'
        rtstates = con.selectAll(sql)
        sql = '''TRUNCATE TABLE rtflightpaths;
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
        states = con.selectAll(sql)
        for sql in FlightPathFactory().buildFlightPathsFromSQL(rtstates, states).sqlInsertGenerator("rtflightpaths"):
            con.execute(sql)
        con.commit()
        con.execute(sql)


def createAirWays(db="LOCAL"):
    """
    Create airways polygon around all previous known positions
    DO NOT USE, polygon too complex for Leaflet to handle
    :param db: The database settings to use
    :return: None
    """
    with Connection(conf=db) as con:
        sql = '''
        TRUNCATE TABLE airways;
        WITH res AS (SELECT id FROM responses
        WHERE to_timestamp(time) >= CURRENT_TIMESTAMP - INTERVAL '3 hours'
        ORDER BY time ASC LIMIT 1)
        , s AS (SELECT * FROM states WHERE response_id >= (SELECT * FROM res)
        AND time_position IS NOT NULL)
        , points AS (SELECT ST_SetSRID(ST_Point(latitude, longitude), 4326) p
        FROM s GROUP BY latitude, longitude)
        INSERT INTO airways (geom)
        SELECT ST_Buffer(ST_Collect(p)::geography, 10000)::geometry FROM points
        '''
        con.execute(sql)


def harvestOpenSky(db="LOCAL"):
    """
    OpenSky Harvest Base function, for use in bot.app.main
    :return: a dictionary containing keys 'success' (boolean) and 'message' (string)
    """
    j = downloadJSON()
    succeed = storeResponse(j, db)
    nstates = len(j["states"])
    # Create flightpaths in post-process thread
    PostProcess(db).start()
    result = {"success": succeed, "message": "Successful harvest, %d aircraft tracked." % nstates}
    return result


class PostProcess(Thread):
    """
    Post-process thread to create flightpaths without interfering with the harvest
    """
    def __init__(self, db="LOCAL"):
        """
        Constructor
        :param db: The database settings to use
        """
        Thread.__init__(self)
        self.db = db

    def run(self):
        """
        Thread implementation. Creates flightpaths.
        :return: None
        """
        createFlightPaths(self.db)
        # Uncomment to enable realtime airways creation, NOT advised.
        # createAirWays(self.db)


def convertToGeoJSON(j):
    """
    convert an OpenSky result to a plottable GeoJSON
    :param j: the JSON object to convert
    :return: A GeoJSON object
    """
    dic = {"type": "FeatureCollection",
           "features": []}
    for state in j["states"]:
        lat = state[6]
        lon = state[5]
        if lat is not None and lon is not None:
            f = {"type": "Feature",
                 "geometry": {"type": "Point",
                              "coordinates": [lon, lat]},
                 "properties": {"id": state[0],
                                "heading": state[-3]}}
            dic["features"].append(f)
    return dic

if __name__ == '__main__':
    r = downloadJSON()
    print r["time"]
    print r["states"][0]
    storeResponse(r)

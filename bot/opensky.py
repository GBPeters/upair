"""
This module contains functions for downloading and storing OpenSky data
"""

# Imports
import json
import urllib2
from thread import start_new_thread

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
    :param The response in a JSON object, as specified on opensky-network.org/apidoc/rest.static
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
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % tuple(strvalues)
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
    with Connection(conf=db) as con:
        sql = '''
        TRUNCATE rtflightpaths;
        INSERT INTO rtflightpaths (icao24, callsign, minres, maxres, mintime, maxtime, geom)
        SELECT r.icao24, r.callsign, min(s.response_id) minres, max(s.response_id) maxres,
        min(s.time_position) mintime, max(s.time_position) maxtime, ST_MakeLine(s.geom) geom FROM rtstates AS r
        LEFT JOIN (select response_id, icao24, callsign, time_position, ST_Point(longitude, latitude) geom FROM states
        WHERE time_position IS NOT NULL AND response_id >= (SELECT id FROM responses
        WHERE to_timestamp(time) > CURRENT_TIMESTAMP - INTERVAL '1 day'
        ORDER BY time asc limit 1) ORDER BY time_position DESC) AS s
        ON r.icao24 = s.icao24 AND r.callsign = s.callsign
        WHERE r.latitude IS NOT NULL
        GROUP BY r.icao24, r.callsign
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
    start_new_thread(createFlightPaths, (db,))
    result = {"success": succeed, "message": "Successful harvest, %d aircraft tracked." % nstates}
    return result


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

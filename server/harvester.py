"""
This module contains functions for downloading and storing OpenSky data
"""

# Imports
import urllib2
import json
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

def storeResponse(response):
    """
    Store
    :param The response in a JSON object, as specified on opensky-network.org/apidoc/rest.html
    :return: Boolean, whether storing has succeeded.
    """
    succeed = False
    with Connection(autocommit=False) as con:
        sql = "INSERT INTO responses (time) VALUES (%d) RETURNING id" % response["time"]
        rid = con.selectOne(sql)[0]
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
            sql = "INSERT INTO states " \
                  "(response_id, icao24, callsign, origin_country, time_position, time_velocity, " \
                  "longitude, latitude, altitude, on_ground, velocity, heading, vertical_rate) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % tuple(strvalues)
            con.execute(sql)
        con.commit()
        succeed = True
    return succeed

if __name__ == '__main__':
    r = downloadJSON()
    print r["time"]
    print r["states"][0]
    storeResponse(r)

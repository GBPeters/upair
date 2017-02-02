"""
Quickfix for states - aircraft link issue,
'Harvester' that just copies all unhandled aircraft from the states table to the aircraft table
DO NOT USE
"""
from db.pghandler import Connection


def copyUnhandledAircraft():
    """
    Copy ICAO24 codes not yet present in aicraft table from states table
    :return: None
    """
    with Connection(autocommit=False) as con:
        sql = "INSERT INTO aircraft (icao24) " \
              "SELECT icao24 FROM states GROUP BY icao24 HAVING icao24 NOT IN " \
              "(SELECT icao24 FROM aircraft) "
        r = con.execute(sql)


def linkAircraft():
    """
    Linker Base function for use in bot.app.main
    :return: A dictionary with keys success (boolean) and message (string)
    """
    copyUnhandledAircraft()
    result = {"success": True,
              "message": "Aircraft codes linked."}
    return result

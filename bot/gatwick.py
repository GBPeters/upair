"""
Module for harvesting data from the
Gatwick Aviation Society (GAS) aircraft database
"""

# Imports
import requests
from bs4 import BeautifulSoup

from db.pghandler import Connection

# Constants
GAS_URL = "http://www.gatwickaviationsociety.org.uk/modeslookup.asp"
GAS_FIELDS = {"Registration": "registration",
              "DICAOType": "icaotype",
              "DType": "type",
              "DSerial": "serial",
              "DOperator": "operator",
              "DICAOOperator": "icaooperator",
              "DSubOperator": "suboperator"}


def downloadGASPage(icao24):
    """
    Search the GAS db for a specific transponder code
    :param icao24: The ICAO24 Mode S transponder code
    :return: The response object
    """
    data = {"MSC": icao24,
            "Submit2": "Find"}
    for key in GAS_FIELDS:
        data[key] = ""
    headers = {"Host": "www.gatwickaviationsociety.org.uk",
               "Accept": "text/static,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US;q=0.7,en;q=0.3",
               "Accept-Encoding": "gzip, deflate",
               "Referer": "http://www.gatwickaviationsociety.org.uk/modeslookup.asp"}
    r = requests.post(GAS_URL, headers=headers, data=data)
    return r


def getMissingICAO24Codes():
    """
    Create a list of codes not yet included in the aircraft database
    :return: A list if ICAO24 Mode S transponder codes
    """
    sql = "SELECT icao24 FROM aircraft WHERE registration IS NULL"
    with Connection() as con:
        codes = [code[0] for code in con.selectAll(sql)]
    return codes


def extractData(rawtext):
    """
    extract values from raw HTML
    :param rawtext: The text to extract from
    :return: a dictionary with the GAS keys and values found in the HTML
    """
    soup = BeautifulSoup(rawtext, "lxml")
    values = {}
    for key in GAS_FIELDS:
        value = soup.find("input", id=key)
        values[key] = value["value"]
    return values


def storeData(icao24, data):
    """
    Store aircraft data into the database
    :param icao24: The ICAO24 Mode S transponder code
    :param data: Dictionary with corresponding data
    :return:
    """
    values = ""
    for key in GAS_FIELDS:
        name = GAS_FIELDS[key]
        value = data[key]
        if value == '' and key != "Registration":
            value = "NULL"
        else:
            value = "'%s'" % value
        values += "%s=%s," % (name, value)
    values = values[:-1]
    sql = "UPDATE aircraft SET %s WHERE icao24='%s'" % (values, icao24)
    with Connection(autocommit=True) as con:
        con.execute(sql)


def harvestGAS():
    """
    GAS Harvest Base function, for use in bot.app.main
    :return: A dictionary with keys success (boolean) and message (string)
    """
    codes = getMissingICAO24Codes()
    if len(codes) > 0:
        code = codes[0]
        r = downloadGASPage(code)
        data = extractData(r.text)
        storeData(code, data)
        if data["Registration"] == "Not Found":
            message = "No aircraft found for ICAO24 code %s" % code
        else:
            message = "Aircraft %s found for ICAO24 code %s." % (data["Registration"], code)
        result = {"success": True,
                  "message": message}
        return result
    else:
        result = {"success": True,
                  "message": "All aircraft already stored in database."}
        return result


if __name__ == "__main__":
    harvestGAS()

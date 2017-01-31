"""
Actual server application
"""

# imports
import sys
from argparse import ArgumentParser
from datetime import datetime
from time import sleep

from bot.gatwick import harvestGAS
from bot.linker import linkAircraft
from bot.opensky import harvestOpenSky
from db.pghandler import CONFIG

HARVEST_INTERVAL = 60
RETRY_INTERVALS = [10, 20, 60]
HARVESTERS = {"opensky": (harvestOpenSky, "OpenSky Harvest Bot"),
              "gatwick": (harvestGAS, "Gatwick Aviation Society Aircraft DB Bot"),
              "linker": (linkAircraft, "ICAO24 Code Linker Quickfix")}
DB = "LOCAL"


def main(harvester, name="Unnamed Bot", interval=HARVEST_INTERVAL, db="LOCAL"):
    """
    Main loop
    :param harvester: The harvest function to use
    :param name: The display name for chosen harvester
    :param interval: The interval to use for harvests
    :return: None
    """
    print "%s started at" % name, datetime.now()
    retry = 0
    waittime = interval
    while True:
        try:
            if retry >= len(RETRY_INTERVALS): retry = len(RETRY_INTERVALS) - 1
            waittime = interval
            errtime = RETRY_INTERVALS[retry]
            try:
                result = harvester(db)
            except KeyboardInterrupt:
                shutDown()
            except Exception, e:
                retry += 1
                printErr("Harvest unsuccessful - " + str(e), errtime)
                waittime = errtime
            else:
                if result['success']:
                    printSuccess(result['message'], interval)
                else:
                    printErr(result['message'], errtime)
        except KeyboardInterrupt:
            shutDown()
        except Exception, e:
            retry += 1
            printErr(str(e), errtime, fatal=True)
            waittime = errtime

        try:
            sleep(waittime)
        except KeyboardInterrupt:
            shutDown()
        except:
            pass


def shutDown():
    """
    Gently shutdown
    :return: None
    """
    print "Shutting down bot..."
    sys.exit(0)

def printErr(message, retry, fatal=False):
    """
    Error print function
    :param message: the message to print
    :param fatal: whether the message is fatal
    :return: None
    """
    t = str(datetime.now())
    error = "FATAL" if fatal else "Error"
    restart = "Restart" if fatal else "Retry"
    p = "%s %s: %s. %s in %d seconds." % (t, error, message, restart, retry)
    print p


def printSuccess(message, nextHarvest=HARVEST_INTERVAL):
    """
    Print successful harvest
    :param response: The download response
    :param nextHarvest: Time in seconds to next harvest
    :return: None
    """
    t = str(datetime.now())
    p = "%s Info: %s Next harvest in %d seconds." % (t, message, nextHarvest)
    print p


def cli():
    """
    Command Line interface for the bot.
    :return: None
    """
    argv = sys.argv[1:]
    argp = ArgumentParser(argv)
    argp.add_argument("bot", choices=HARVESTERS.keys(),
                      help="name of the bot to use")
    argp.add_argument("--interval", "-i", default=HARVEST_INTERVAL, type=int, help="harvest interval in seconds")
    argp.add_argument("--db", "-d", default="LOCAL", choices=CONFIG.keys(), help="the database config setting to use.")
    pargs = argp.parse_args(argv)
    fun, name = HARVESTERS[pargs.bot]
    main(fun, name, pargs.interval, pargs.db)


if __name__ == "__main__":
    cli()

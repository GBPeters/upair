"""
Actual server application
"""

# imports
import sys
from datetime import datetime
from time import sleep

from bot.gatwick import harvestGAS
from bot.linker import linkAircraft
from bot.opensky import harvestOpenSky

# Constants
HARVEST_INTERVAL = 60
RETRY_INTERVALS = [10, 20, 60]
HARVESTERS = {"opensky": (harvestOpenSky, "OpenSky Harvest Bot"),
              "gatwick": (harvestGAS, "Gatwick Aviation Society Aircraft DB Bot"),
              "linker": (linkAircraft, "ICAO24 Code Linker Quickfix")}


def main(harvester, name="Unnamed Bot", interval=HARVEST_INTERVAL):
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
                result = harvester()
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
    argv = sys.argv
    if len(argv) != 2 and len(argv) != 3:
        sys.exit("Invalid arguments. Please choose botname.")
    if argv[1] not in HARVESTERS:
        print "Listed bots:"
        for b in HARVESTERS:
            print "%s - %s" % (b, HARVESTERS[b][1])
            sys.exit("Please choose a bot from the list.")
    if len(argv) == 3:
        try:
            interval = int(argv[2])
            if interval < 0: interval = 0
        except:
            sys.exit("Interval is not a number.")
    else:
        interval = HARVEST_INTERVAL

    botname = sys.argv[1]
    fun, name = HARVESTERS[botname]
    main(fun, name, interval)


if __name__ == "__main__":
    cli()

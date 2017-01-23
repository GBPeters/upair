"""
Actual server application
"""

# imports
import sys
from datetime import datetime
from time import sleep

from bot.opensky import harvest

# Constants
HARVEST_INTERVAL = 60
RETRY_INTERVALS = [10, 20, 60]
HARVESTERS = {"opensky": (harvest, "OpenSky Harvest Bot")}


def main(harvester, name="Unnamed Bot"):
    """
    Main loop
    :return: None
    """
    print "%s started at" % name, datetime.now()
    retry = 0
    while True:
        if retry >= len(RETRY_INTERVALS): retry = len(RETRY_INTERVALS) - 1
        waittime = HARVEST_INTERVAL
        errtime = RETRY_INTERVALS[retry]
        try:
            try:
                result = harvester()
            except KeyboardInterrupt:
                raise
            except Exception, e:
                retry += 1
                printErr("Harvest unsuccessful - " + str(e), errtime)
                waittime = errtime
            else:
                if result['success']:
                    printSuccess(result['message'])
                else:
                    printErr(result['message'], errtime)
        except KeyboardInterrupt:
            raise
        except Exception, e:
            retry += 1
            printErr(str(e), errtime, fatal=True)
            waittime = errtime
        sleep(waittime)

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


def printSuccess(message):
    """
    Print successful harvest
    :param response: The download response
    :return: None
    """
    t = str(datetime.now())
    p = "%s Info: %s Next harvest in %d seconds." % (t, message, HARVEST_INTERVAL)
    print p


def cli():
    argv = sys.argv
    if len(argv) != 2:
        sys.exit("Invalid arguments. Please choose botname.")
        quit()
    if argv[1] not in HARVESTERS:
        print "Listed bots:"
        for b in HARVESTERS:
            print "%s - %s" % (b, HARVESTERS[b][1])
            sys.exit("Please choose a bot from the list.")
    botname = sys.argv[1]
    fun, name = HARVESTERS[botname]
    main(fun, name)


if __name__ == "__main__":
    cli()

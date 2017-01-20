"""
Actual server application
"""

# imports
from datetime import datetime
from time import sleep
from server.harvester import downloadJSON, storeResponse

# Constants
HARVEST_INTERVAL = 60
RETRY_INTERVALS = [10, 20, 60]

def main():
    """
    Main loop
    :return: None
    """
    print "OpenSky Harvest Server started at", datetime.now()
    retry = 0
    while True:
        if retry >= len(RETRY_INTERVALS): retry = len(RETRY_INTERVALS) - 1
        waittime = HARVEST_INTERVAL
        errtime = RETRY_INTERVALS[retry]
        try:
            try:
                r = downloadJSON()
            except KeyboardInterrupt:
                raise
            except Exception, e:
                retry += 1
                printErr("Download unsuccessful - " + str(e), errtime)
                waittime = errtime
            else:
                try:
                    if storeResponse(r):
                        printSuccess(r)
                        retry = 0
                    else:
                        retry += 1
                        printErr("Storing unsuccessful", errtime)
                        waittime = errtime
                except KeyboardInterrupt:
                    raise
                except Exception, e:
                    retry += 1
                    printErr("Storing unsuccessful - " + str(e), errtime)
                    waittime = errtime
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

def printSuccess(response):
    """
    Print successful harvest
    :param response: The download response
    :return: None
    """
    t = str(datetime.now())
    p = "%s Info: Successful harvest, %d aircraft tracked. Next harvest in %d seconds." % (t, len(response["states"]), HARVEST_INTERVAL)
    print p


if __name__ == "__main__":
    main()
# PYTHONPATH
import os.path as path
import sys

projfolder = path.dirname(path.dirname(path.realpath(__file__)))
sys.path.append(projfolder)

#imports
from argparse import ArgumentParser

from db.pghandler import CONFIG
from map.mapserver import start


def cli():
    argv = sys.argv[1:]
    argp = ArgumentParser(argv)
    argp.add_argument("--host", "-H", default="localhost", help="host address")
    argp.add_argument("--db", "-d", default="LOCAL", choices=CONFIG.keys(), help="the database config setting to use.")
    pargs = argp.parse_args(argv)
    start(pargs.db, pargs.host)

if __name__ == '__main__':
    cli()

# TODO - Check if it is easy and worth it to use readline to have a command history

import argparse
import json
import logging.config
import os

import TCX

COMMANDS_HELP = {"print": "Prints main activity currently loaded in memory",
                 "tcx2mem":"Loads an activity from a TCX file to memory",
                 "quit":"Quits the command line",
                 "help":"Shows list of recognised commands"}

def main():

    # Initialise command session variables
    entered = ""
    main_activity = None

    while entered != "quit":
        entered = input(">> ")
        entered_words = entered.split()
        command = entered_words[0]
        args = entered_words[1:]

        if command not in COMMANDS_HELP:
            print ("Command not recognised. For a list of recognised commands enter 'help'")
            continue
        if command == "help":
            [print("   "+c+" - "+h) for (c,h) in COMMANDS_HELP.items()]
        elif command == "tcx2mem":
            print("Called {} command with args {}".format(command,args))
            if len(args) != 1:
                print ("   Error in call to 'tcx2mem': 'tcx2mem' takes 1 argument with the path to the TCX file")
            main_activity = TCX.parse(args[0])
        elif command == "print":
            if main_activity is None:
                print ("   No activity loaded")
            else:
                print (main_activity)


def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#    parser.add_argument('tcx_file1', type=argparse.FileType('r'))
#    parser.add_argument('-c', '--cutoff', type=int, default=10,
#                        help="cutoff distance in meters for similar points")
#    parser.add_argument('-e', '--even', type=int,
#                        help="evenly distribute points in meters")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    setup_logging()

    main()
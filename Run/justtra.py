# TODO - Check if it is easy to use a CLI module to make this cmd or cmd2

import argparse
import json
import logging.config
import os

import TCX
import activities
import athletes

COMMANDS_HELP = {"print": "Prints main activity currently loaded in memory",
                 "tcx2mem":"Loads an activity from a TCX file to memory",
                 "athl": "Creates and ahtlete",
                 "add" : "Adds activity in memory to active athlete",
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
            if len(args) != 1:
                print ("   Error in call to 'tcx2mem': 'tcx2mem' takes 1 argument with the path to the TCX file")
                continue
            main_activity = activities.run(TCX.parse(args[0]))
            print ("Activity loaded: {}".format(main_activity))
        elif command == "athl":
            print("Called {} command with args {}".format(command,args))
            active_athlete = athletes.athlete()
            print ("Athlete created: {}".format(active_athlete))
        elif command == "add":
            print("Called {} command with args {}".format(command,args))
            if main_activity is None:
                print ("    Error: No activity loaded in memory")
                continue
            active_athlete.add_activity(main_activity)
            print ("Activity {} addedto athlete {}".format(main_activity,active_athlete))
        elif command == "print":
            if main_activity is None:
                print ("   No activity loaded")
            elif len(args) == 0:
                main_activity.print()
            else:
                main_activity.print(int(args[0]))

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
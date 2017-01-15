
# LEGEND
# Normal comment
# ## TEMPORAL - Working solution but needs to be revisited for a more complete implementation
# ### HARDCODED - Hardcoded value in case it needs to be revisited in the future

# #### Log of next steps:
#       - TODO Eliminate main and test in a different file
#       - TODO Change the logging formatter to produce logs in JSON format
#       - TODO Prepare a few cases of automated testing (paused exercise in the tests, several laps, missing data ...)
#       - TODO Process all tracks in each lap (several tracks mean the exercise was paused)
#       - TODO Some TCX files have laps with no track - not sure if it's valid or not

import argparse
import logging
import xml.etree.ElementTree as ET

import dateutil.parser

NA_VALUE = None
HEADERS = ("timestamp", "lap", "latitude", "longitude", "altitude", "distance", "heartrate", "cadence", "power")


def main():
    FILE = args.tcx_file1

    smpl_lst = parse(FILE)

    # Print a list of samples as CSV
    for smpl in smpl_lst:
        for item in smpl:
            print(str(item)+", ",end="")
        print("")


def parse(filename):
    """Parse .tcx file. Return list of samples in the activity.

    :param filename: Name of the file to process
    :return: List of tuples with first tuple being the headers and remaining being sample points.
    """
    # Get logger for this module and log "entering" event
    logger = logging.getLogger(__name__)
    logger.info("Entering TCX parse to process %s", filename)

    # Define Constants
    ns = {"df": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
          "ext": "http://www.garmin.com/xmlschemas/ActivityExtension/v2"}  # Dictionary of namespaces to simplify future calls

    # Initialise variables
    smpl_lst = []

    # Parse the xml file
    logger.debug("Calling ET.parse(%s)", filename)
    try:
        tree = ET.parse(filename)
    except Exception as e:  # ## NEED TO CAPTURE THE EXCEPTION THAT WAS RAISED AND PROPAGATE IT
        logger.error("Error parsing the file", exc_info=True)
        raise e
    root = tree.getroot()

    # Get the list of activities in the file and if there is more than 1 activity, raise an exception
    logger.debug("""Extracting "Actvities" and "Activity" nodes""")
    acts_nds = root.findall("df:Activities", ns)
    if len(acts_nds) != 1:
        logger.error("""ERROR IN TCX FILE: More than 1 "Activities" node in the file""")
        raise ValueError("""ERROR IN TCX FILE: More than 1 "Activities" node in the file""")
    act_lst = acts_nds[0].findall("df:Activity",
                                  ns)  ### HARDCODED: process first "Activities" (Would have been raised exception if more than 1)
    if len(act_lst) != 1:
        logger.error("""ERROR IN TCX FILE: More than 1 "Activity" node in the file""")
        raise ValueError("""ERROR IN TCX FILE: More than 1 "Activity" node in the file""")

    # Process the first activity
    activity = act_lst[0]  ### HARDCODED process first activity (Would have been raised exception if more than 1)
    sport = activity.attrib["Sport"]  # Get the sport from the "Sport" attribute in the "Activity" node
    datetime = activity.find("df:Id",
                             ns).text  # Get the date and time from the text in the Id element inside the "Activity" node
    laps_lst = activity.findall("df:Lap", ns)  # Build a list with all the laps
    logger.debug("Processing activity - DateTime: %s - Sport: %s - Laps: %s", datetime, sport, len(laps_lst))

    # Process the laps in the activity
    for lap_nmbr in range(len(laps_lst)):
        logger.debug("Starting to process lap: lap_nmbr %s", lap_nmbr)
        trck_lst = laps_lst[lap_nmbr].findall("df:Track", ns)

        # ## To deal with pauses need to create a "paused/active" flag and fill in the space between tracks with "paused" samples
        trck_nmbr = 0  # ## TEMPORAL - NEED TO PROCESS ALL TRACKS IN FINAL VERSION##
        # Extract information of all points in the Lap
        pnts_lst = trck_lst[trck_nmbr].findall("df:Trackpoint", ns)
        logger.debug("Startint to process points: lap_nmbr: %s - trck_nmbr: %s of %s - points:%s", lap_nmbr, trck_nmbr,
                     len(trck_lst) - 1, len(pnts_lst))
        point_number = 0
        for point in pnts_lst:
            # Timestamp (If not available raise exception with invalid file)
            try:
                pnt_timestamp = point.find("df:Time", ns).text
                pnt_timestamp = dateutil.parser.parse(pnt_timestamp)
            except AttributeError:
                raise ValueError("""ERROR IN TCX FILE: TrackPoint with no timestamp""")
            # GPS coordinates
            pnt_pos = point.find("df:Position", ns)
            try:
                pnt_lat = pnt_pos.find("df:LatitudeDegrees", ns).text
                pnt_lat = float(pnt_lat)
            except AttributeError:
                pnt_lat = NA_VALUE
            try:
                pnt_long = pnt_pos.find("df:LongitudeDegrees", ns).text
                pnt_long = float(pnt_long)
            except AttributeError:
                pnt_long = NA_VALUE
            # Altitude
            try:
                pnt_altitude = point.find("df:AltitudeMeters", ns).text
                pnt_altitude = float(pnt_altitude)
            except AttributeError:
                pnt_altitude = NA_VALUE
            # Distance covered since begining of activity
            try:
                pnt_dist = point.find("df:DistanceMeters", ns).text
                pnt_dist = float(pnt_dist)
            except AttributeError:
                pnt_dist = NA_VALUE
            # Instantaneous Heart Rate
            pnt_hr_elmnt = point.find("df:HeartRateBpm", ns)
            try:
                pnt_hr = pnt_hr_elmnt.find("df:Value", ns).text
                pnt_hr = int(pnt_hr)
            except AttributeError:
                pnt_hr = NA_VALUE
            # Instantaneous cadence
            pnt_cad_elmnt = point.find("df:Cadence", ns)
            try:
                pnt_cad = pnt_cad_elmnt.text
                pnt_cad = int(pnt_cad)
            except AttributeError:
                pnt_cad = NA_VALUE

            # Process extensions
            pnt_ext = point.find("df:Extensions", ns)
            if not pnt_ext is None:
                # Instantaneous running power
                pnt_tpx = pnt_ext.find("ext:TPX", ns)
                try:
                    pnt_pow = pnt_tpx.find("ext:Watts", ns).text
                    pnt_pow = int(pnt_pow)
                except AttributeError:
                    pnt_pow = NA_VALUE
            else:
                pnt_pow = NA_VALUE

            # If it is the first point of the first lap, store headers tuple
            if len(smpl_lst) == 0:
                smpl_lst.append(HEADERS)

            # Create a tuple with sample informationand store in a list
            smpl = (pnt_timestamp, lap_nmbr + 1, pnt_lat, pnt_long, pnt_altitude, pnt_dist, pnt_hr, pnt_cad, pnt_pow)
            smpl_lst.append(smpl)
            point_number = point_number + 1
            logger.debug ("Processed point: {}".format(point_number))
        logger.debug("Finished processing points: lap_nmbr: %s - trck_nmbr: %s of %s", lap_nmbr, trck_nmbr,
                     len(trck_lst) - 1)
    logger.info("Finished TCX parse to process %s", filename)

    return  smpl_lst

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tcx_file1', type=argparse.FileType('r'))
    parser.add_argument('tcx_file2', type=argparse.FileType('r'))
    parser.add_argument('-c', '--cutoff', type=int, default=10,
                        help="cutoff distance in meters for similar points")
    parser.add_argument('-e', '--even', type=int,
                        help="evenly distribute points in meters")
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()

    print(args.tcx_file1)

    main()
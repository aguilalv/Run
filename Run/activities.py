import pandas as pd

# TODO: Complete __str__ method to return a description of the activity

class activity:

    """Generic activity class from which the different types (e.g. run, bike ...) can inherit

    """

    def __init__(self,raw_smpl_lst):
        """Construct an activity objet

        :param raw_smpl_lst: List of tuples with first element being a tuple with headers and subsequent being tuple of strings with sample data
        """
        self.df = pd.DataFrame(
            raw_smpl_lst[1:],
             columns=raw_smpl_lst[0])

    def print(self,num_samples=None):
        if num_samples == None:
            num_samples = len(self.df)
        print (self.df.head(num_samples))


    def __str__(self):
        return ("Activity xxx on xx.xx.xx with xxx samples")

#    @classmethod
#    def fromFile(cls,filename):
#        cls.

class run(activity):

    """Run class to represent a run training activity. Inherits from activity.

    """

    def __init__(self,raw_smpl_lst):
        activity.__init__(self,raw_smpl_lst)
        self._calculate_fields()

    def _calculate_fields(self):
        """ Calculate running specific metrics derived from the raw data"""

        # TODO: Clean df to make sure all samples are 1 sec apart. Right now Asumes all samples are 1 second apart.
        #           A possible way to do this is to create a list of timestamp values separated 1 second apart and reindexing (see http://pandas.pydata.org/pandas-docs/stable/missing_data.html)
        #           Another way (probably better) is to move the keys to a column and use fillna (see same page in datetime section)
        # TODO: Calculate levelpace and levelspeed. right now levelpace is same as pace

        # Calculate speed in km/h
        self.df['speed'] = (self.df['distance'] - self.df['distance'].shift(1)) * 3.6
        # calculate pace in seconds / Km
        self.df['pace'] = 3600 / self.df['speed']
        # calculate slope in % (100 * rise / run)
        self.df['slope'] = ((self.df['altitude'] - self.df['altitude'].shift(1)) / (self.df['distance'] - self.df['distance'].shift(1))) * 100
        # calculate level pace in seconds / Km
        self.df['levelpace'] = self.df['pace']
        # calculate level speed in seconds / Km
        self.df['levelspeed'] = self.df['speed']


        # Calculate filter for running and stopped samples
        self.df['state'] = "Stopped"
        self.df.ix[self.df.speed > 4, 'state'] = "Running"

    def drift(self,minutes=None):
        """Calculate drift for duration of x minutes

        :return:
        """
        # TODO calculate drift for a specific duration. Right now calculates first half vs second half

        # Calculate drift
        half1 = self.df[self.df.state == "Running"][:(len(self.df) // 2)]
        half2 = self.df[self.df.state == "Running"][(len(self.df) // 2):]
        return ((half2.heartrate / half2.levelspeed).mean()) / ((half1.heartrate / half1.levelspeed).mean()) - 1

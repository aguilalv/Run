import pandas as pd

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
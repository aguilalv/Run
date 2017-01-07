class activity:

    """Generic activity class from which the different types (e.g. run, bike ...) can inherit

    """

    def __init__(self,raw_smpl_lst):
        """Construct an activity objet

        :param raw_smpl_lst: List of tuples with first element being a tuple with headers and subsequent being tuple of strings with sample data
        """
        self.headers = raw_smpl_lst[0]
        self.raw_smpl_lst = raw_smpl_lst[1:]

    def print(self,num_samples=None):
        if num_samples == None:
            num_samples = len(self.raw_smpl_lst)

        print (self.headers)
        for i in range(num_samples):
            print(self.raw_smpl_lst[i])

    def __str__(self):
        return ("Activity xxx on xx.xx.xx with xxx samples")

#    @classmethod
#    def fromFile(cls,filename):
#        cls.
import math

class coord:

    """Geographic coordinates of a point.

    """


    def __init__(self,lat,long):
        """Construct a coordinates instance.

        Args:
            lat (float): Lattitude
            long (float): Longitude
        """
        self.lat = lat
        self.long = long
        
    def __sub__(self, other):
        """Return linear distance between self and another point.

        (May be change to return geographic distance? May be not needed if points are close?)

        Args:
            other (:obj: 'coord'): Point to which calculate distance

        Returns:
            Absolute distance between self and other point.


        """
        ret = math.sqrt(((other.lat - self.lat)**2) + ((other.long - self.long)**2))
        return abs(ret)
        
    
    def __str__(self):
        ret = '({: .5f},{: .5f})'.format(self.lat,self.long)
        return ret
        

class test_coord:
    
    def __init__(self,char):
        self.char = char
        
    def __sub__(self, other):
        # return -2 if different and 1 if equal
        if self.char == other.char:
            ret = 1
        else:
            ret = -2
        return ret
        
    
    def __str__(self):
        ret = self.char
        return ret
        

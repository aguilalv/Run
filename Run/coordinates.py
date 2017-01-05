import math

class coord:
    
    def __init__(self,lat,long):
        self.lat = lat
        self.long = long
        
    def __sub__(self, other):
        # ## Returns linear distance (May be change to return geographic distance? May be not needed if points are close?)
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
        

import os

class player(object):
    def __init__(self,features):
        self.code = features[0]
        self.last = features[1]
        self.first = features[2]
        self.bat = features[3]
        self.throw = features[4]
        self.team = features[5]
        self.pos = features[6]
        self.k = 0
        self.bb = 0
        self.s = 0
        self.d = 0
        self.t = 0
        self.hr = 0
        self.pa = 0

    def __str__(self):
        return '{} {} {} {}'.format(
            self.first, self.last, self.pos, self.team        
        )


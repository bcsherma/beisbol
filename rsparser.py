import os
import re
from copy import deepcopy

# get a list of files in the event directory
files = os.listdir('2016eve')
# open and read the rosters
pfiles = [f for f in files if f[-4:] == '.ROS']
pfiles = [open('2016eve/'+f).readlines() for f in pfiles]

# object for storing player information
class player(object):
    def __init__(self,features):
        # these are attributes we get from the line
        self.code = features[0]
        self.last = features[1]
        self.first = features[2]
        self.bat = features[3]
        self.throw = features[4]
        self.team = features[5]
        self.pos = features[6]
        # these are attributes we initialize to zero
        self.k = 0
        self.bb = 0
        self.s = 0
        self.d = 0
        self.t = 0
        self.hr = 0
        self.pa = 0

# initialize an empty dictionaries of players
# keys are the player code
players = {}

# for every line of the file
# try to initialize a player if we
# haven't already created that player
# for a different team
for f in pfiles:
    for p in f:
        tmp = player(p.strip().split(','))
        if tmp.code in players:
            continue
        players[tmp.code] = tmp

# cull the list of files to only be
# event files
files = [
    f for f in files if f[-4:] == '.EVA' or f[-4:] == '.EVN'
]
files = [open('2016eve/'+f).readlines() for f in files]
# concatenate all the events into one list
files = sum(files,[])


# these variables are used to keep track
# of the current batter, home pitcher,
# and visiting pitcher
hp = None
ap = None
batter = None

# an enumeration of the outcomes we
# want to want to track
class outcome:
    nothing = -1
    out = 0
    single = 1
    double = 2
    triple = 3
    hr = 4
    walk = 5
    strikeout = 6


single = re.compile(r'S[0-9]+')
double = re.compile(r'D[0-9]+')
triple = re.compile(r'T[0-9]+')
homer = re.compile(r'[H|HR][0-9]*')
walk = re.compile(r'[W|I|IW]')
strikeout = re.compile(r'K')


def getResult(line):
    if line[0].isdigit():
        return outcome.out
    line = line.replace(';','/')
    line = line.replace('.','/')
    line = line.replace('-','/')
    line = line.replace('+','/')
    line = line.split('/')[0]
    line = line.strip()
    if not line or line == 'NP':
        return outcome.nothing
    if single.match(line):
        #print('single',line)
        return outcome.single
    if double.match(line):
        #print('double',line)
        return outcome.double
    if triple.match(line):
        #print('triple',line)
        return outcome.triple
    if homer.match(line):
        #print('homer',line)
        return outcome.hr
    if walk.match(line):
        #print('walk',line)
        return outcome.walk
    if strikeout.match(line):
        #print('strikeout',line)
        return outcome.strikeout
    return outcome.nothing


# iterate over the events and sum up
# everything that happens
for line in files:
    line = line.split(',')
    # check to see if there is a roster change
    if line[0] in {'start','sub'}:
        if players[line[1]].pos == 'P':
            if line[3] == '0':
                ap = players[line[1]]
            else:
                hp = players[line[1]]
        # keep track of whether or not the current
        # player is a home player or not
        players[line[1]].home = line[3]
    # check to see if there is a play
    if line[0] == 'play':
        result = getResult(line[6])
        continue
        batter = players[line[3]]
        if batter.pos == 'P':
            batter = deepcopy(batter)
        if batter.home == '1':
            pitcher = ap
        else:
            pitcher = hp
        batter = players[line[3]]

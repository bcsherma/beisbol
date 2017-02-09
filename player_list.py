import os
from player import player
from copy import deepcopy

def uninvolved(string):
    if 'K' in string:
        if 'BK' not in string:
            return False
    if 'NP' in string: return True
    if 'BK' in string: return True
    if 'CS' in string: return True
    if 'DI' in string: return True
    if 'OA' in string: return True
    if 'PB' in string: return True
    if 'WP' in string: return True
    if 'PO' in string: return True
    if 'POCS' in string: return True
    if 'SB' in string: return True
    return False

files = os.listdir('2016eve')
pfiles = [f for f in files if f[-4:] == '.ROS']
pfiles = [open('2016eve/'+f).readlines() for f in pfiles]

players = {}

for f in pfiles:
    for p in f:
        tmp = player(p.strip().split(','))
        if tmp.code in players:
            continue
        players[tmp.code] = tmp

files = os.listdir('2016eve')
files = [f for f in files if f[-4:] == '.EVA' or f[-4:] == '.EVN']
files = [open('2016eve/'+f).readlines() for f in files]

files = sum(files,[])

hp = 0
ap = 0

for line in files:
    line = line.split(',')
    if line[0] in {'start','sub'}:
        if players[line[1]].pos == 'P':
            if line[3] == '0':
                ap = players[line[1]]
            else:
                hp = players[line[1]]
        players[line[1]].home = line[3]
    
    if line[0] == 'play':
        if uninvolved(line[6].split('/')[0]): 
            continue
        batter = players[line[3]]
        if batter.pos == 'P':
            batter = deepcopy(batter)
        if batter.home == '1':
            pitcher = ap
        else:
            pitcher = hp
        
        batter.pa += 1
        pitcher.pa += 1

        event = line[6].split('/')[0]

        if 'W' in event:
            batter.bb += 1
            pitcher.bb += 1
        elif 'K' in event:
            batter.k += 1
            pitcher.k += 1
        elif 'S' in event:
            batter.s += 1
            pitcher.s += 1
        elif 'D' in event:
            batter.d += 1
            pitcher.d += 1
        elif 'T' in event:
            batter.t += 1
            pitcher.t += 1
        elif event[:2] == 'HR':
            batter.hr += 1
            pitcher.hr += 1
        else:
            pass

for p in players:
    pl = players[p]
    print pl, pl.pa ,pl.k, pl.bb, pl.s, pl.d, pl.t, pl.hr


# imports
import re, os, os.path

# data structure for storing players
class player:
	def __init__(self,id,last,first,bats,throws,team,pos):
		self.id = id
		self.last = last
		self.first = first
		self.bats = bats
		self.throws = throws
		self.team = team
		self.pos = pos

	# return a string representation
	def __repr__(self):
		return '{} {} {} {}'.format(
			self.last,self.first,self.team,self.pos
		)

	# compare this player to another player
	def __eq__(self,other):
		return self.id == other.id

# given a RS directory return the players
# from the season
def getPlayers(directory):
	# make sure this directory exists
	assert os.path.isdir(directory)
	files = [
		directory+'/'+f for f in os.listdir(directory) \
		if f.endswith('.ROS')
	]
	playerSrc = sum([open(f).readlines() for f in files],[])
	playerSrc = [l.strip().split(',') for l in playerSrc]
	players = [player(*p) for p in playerSrc]
	return {p.id:p for p in players}

# a data structure for storing the details of an event
# in a game of baseball
class event:
	# constructor
	def __init__(self,hitter,pitcher,count,seq,outcome):
		print(hitter,pitcher,outcome)
		pass

# data structure for storing all information about
# a single baseball game
class game:
	# constructor
	def __init__(self,events,players):
		# process the event log
		self.processEvents(events,players)
	
	def processEvents(self,events,players):
		# this dictionary will contain information about
		# the game
		self.info = {}
		# this is an ordered list of the events of the game
		self.events = []
		# sets of player id's
		self.homeplayers = set()
		self.awayplayers = set()
		# these variables keep track of the state of the game
		awaypitcher = None
		homepitcher = None
		# iterate over the contents of the event log and update
		# information about the game
		for e in events:
			e = e.strip().split(',')
			if e[0] == [id]:
				self.id = e[1]
			# add this to the info dictioanry
			elif e[0] == 'info':
				_,category,detail = e
				self.info[category] = detail
			# keep track of the starters
			elif e[0] == 'start' or e[0] == 'sub':
				_,pid,_,team,bo,pos = e
				# update the rosters
				if int(team):
					self.homeplayers.add(pid)
					if int(pos) == 1:
						homepitcher = pid
				else:
					self.awayplayers.add(pid)
					if int(pos) == 1:
						awaypitcher = pid
			elif e[0] == 'play':
				_,_,half,hitter,count,seq,outcome = e
				if outcome == 'NP': continue
				if int(half) == 1:
					pitcher = awaypitcher
				else:
					pitcher = homepitcher
				# add a new event to the game
				self.events.append(
					event(hitter,pitcher,count,seq,outcome)
				)
			

# given a RS directory return all events from the season
def getEvents(directory,players):
	# make sure this directory exists
	assert os.path.isdir(directory)
	files = [	
		directory+'/'+f for f in os.listdir(directory) \
		if f.endswith('.EVN') or f.endswith('.EVA')
	]
	events = sum([open(f).readlines() for f in files],[])
	index = 0
	games = []
	while(True):
		if index == len(events):
			break
		if events[index].split(',')[0] == 'id':
			stop = index + 1
			while(True):
				if stop == len(events):
					break
				if events[stop].split(',')[0] == 'id':
					break
				stop += 1
			games.append(game(events[index:stop],players))
		# increment
		index += 1

if __name__ == '__main__':
	players = getPlayers('2009eve')
	events = getEvents('2009eve',players)


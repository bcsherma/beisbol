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

# regular expressions for event parsing
eventStr 	= re.compile(r'([\w]+)[;/()+-]?')
modifierStr = re.compile(r'/([\w]+)')
gbStr 		= re.compile(r'BG[\w]*|G[\w]*')
ldStr 		= re.compile(r'BL[\w]*|L[\w]*')
fbStr 		= re.compile(r'BP[\w]*|F|FDP|IF|P|SF')
outStr 		= re.compile(r'[0-9].*|E[0-9]+|FC[0-9]+|FLE[0-9]+')
singleStr	= re.compile(r'S[0-9]+')
doubleStr 	= re.compile(r'D[0-9]+|DGR')
tripleStr 	= re.compile(r'T[0-9]+')
homerStr 	= re.compile(r'H[R]?[0-9]*')
kStr 		= re.compile(r'K.*')
walkStr 	= re.compile(r'HP|IW?|W')

# a data structure for storing the details of an event
# in a game of baseball
class event:
	# static fields for ab result
	out 	= 0
	single 	= 1
	double 	= 2
	triple 	= 3
	hr 		= 4
	k 		= 5
	bb 		= 6
	
	# ab results for contact
	none 	= 1
	fly 	= 2
	ground 	= 3
	line 	= 4

	# constructor
	def __init__(self,id,hitter,pitcher,count,seq,outcome):
		# save the id of the game this event happens in
		self.game = id
		# save pitcher and hitter during this event
		self.pitcher = pitcher
		self.hitter = hitter
		# assume no contact
		self.contact = event.none
		# match the event string
		result = eventStr.match(outcome)
		contact = modifierStr.search(outcome)
		# assert the event string is valid
		assert result is not None
		result = result.group(1)
		# if there is contact figure out what kind
		if contact is not None:
			contact = contact.group(1)
			if gbStr.fullmatch(contact):
				self.contact = event.ground
			elif ldStr.fullmatch(contact):
				self.contact = event.line
			elif fbStr.fullmatch(contact):
				self.contact= event.fly
		# check for all at bat outcomes, assuming either 
		# a batted ball, k, or walk
		if outStr.fullmatch(result):
			self.outcome = event.out
		elif kStr.fullmatch(result):
			self.outcome = event.k
		elif walkStr.fullmatch(result):
			self.outcome = event.bb
		elif singleStr.fullmatch(result):
			self.outcome = event.single
		elif doubleStr.fullmatch(result):
			self.outcome = event.double
		elif tripleStr.fullmatch(result):
			self.outcome = event.triple
		elif homerStr.fullmatch(result):
			self.outcome = event.hr





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
			if e[0] == 'id':
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
					event(self.id,hitter,pitcher,count,seq,outcome)
				)
			

# given a RS directory return all events from the season
def getGames(directory,players):
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
	return {g.id:g for g in games}


if __name__ == '__main__':
	players = getPlayers('2009eve')
	games = getGames('2009eve',players)
	


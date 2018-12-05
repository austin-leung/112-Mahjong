# logic.py containsb methods evaluating whether melds are legal as well as the score of hands

# returns if a list of three tiles is a Pong
def isPong(lst):
	if len(lst) != 3: # pong is 3 elements
		return False
	# all elements must be the same 
	elif lst[0] == lst[1] and lst[1] == lst[2]: 
		return True
	return False

# returns if a list of four tiles is a Pong
def isKong(lst):
	if len(lst) != 4: # kong is 4 elements
		return False
	# all elements must be the same 
	elif lst[0] == lst[1] and lst[1] == lst[2] and lst[2] == lst[3]: 
		return True
	return False

# returns if a list of three tiles is a Chow
def isChow(lst):
	if len(lst) != 3: 
		return False
	sortedTiles = sorted(lst)
	typeTiles = []
	numTiles = []
	for i in range(3):
		filename = sortedTiles[i]
		# first element being a digit indicates it is a dot, bamboo, or character
		if filename[0] not in "0123456789":
			return False
		typeTiles.append(filename[1:]) # should be "dot", "bamboo", or "character"
		numTiles.append(filename[0:1]) # should be 1, 2, 3, ... , 9
	# check if same type (e.g. "dot", "dot", "dot")
	if typeTiles[0] != typeTiles[1] or typeTiles[1] != typeTiles[2]:
		return False
	# check if consecutive run (e.g. 4, 5, 6)
	if int(numTiles[0]) + 1 != int(numTiles[1]) or int(numTiles[1]) + 1 != int(numTiles[2]): 
		return False
	return True

# returns a list of melds that are possible from a list of tiles 
def possibleMelds(tileLst):
	solutionLst = []
	trios = threeFourPowerset(tileLst)[0]
	quads = threeFourPowerset(tileLst)[1]
	for trio in trios:
		if isChow(trio):
			trio.append("Chow")
			solutionLst.append(sorted(trio))
		elif isPong(trio):
			trio.append("Pong")
			solutionLst.append(trio)
	for quad in quads:
		if isKong(quad):
			quad.append("Kong")
			solutionLst.append(quad)
	# get rid of duplicates
	solutionSet = set()
	for item in solutionLst:
		solutionSet.add(tuple(item))
	return solutionSet

# powerset from course notes
def powerset(tileLst):
    # returns a list of all subsets of the list a
    if (len(tileLst) == 0):
        return [[]]
    else:
        allSubsets = [ ]
        for subset in powerset(tileLst[1:]):
            allSubsets += [subset]
            allSubsets += [[tileLst[0]] + subset]
        return allSubsets

# adapted powerset returning sets of length 3 and 4
def threeFourPowerset(tileLst):
 	psets = powerset(tileLst)
 	threeLst = []
 	fourLst = []
 	for lst in psets:
 		if len(lst) == 3:
 			threeLst.append(lst)
 		if len(lst) == 4:
 			fourLst.append(lst)
 	return [threeLst, fourLst]

 # adapted powerset returning sets of length 3
def threePowerset(tileLst):
 	psets = powerset(tileLst)
 	threeLst = []
 	for lst in psets:
 		if len(lst) == 3:
 			threeLst.append(lst)
 	return threeLst

import copy
# recursive backtracking to find a winning combo from tiles, returns None if no win
def winningCombo(tileLst, winCombo = None):
	if winCombo == None:
		winCombo = []
	# final combo should always be a winning pair, not a meld
	if len(tileLst) == 2 and tileLst[0] == tileLst[1]:
		return winCombo + tileLst
	else:
		for threeSet in threePowerset(tileLst):
			if isPong(threeSet) or isChow(threeSet):
				newWinCombo = winCombo + threeSet
				newTileLst = tileLst[:]
				for tile in threeSet:
					newTileLst.remove(tile)
				tmp = winningCombo(newTileLst, newWinCombo)
				if tmp != None:
					return tmp
	return None

# recursive backtracking to find the longest possible combo from tileLst
# may return a winning combo if possible
def longestCombo(tileLst, winCombo = None, curLongCombo = None):
	if winCombo == None:
		winCombo = []
		curLongCombo = []
	# final combo should always be a winning pair, not a meld
	if len(tileLst) == 2 and tileLst[0] == tileLst[1]:
		return curLongCombo
	else:
		for threeSet in threePowerset(tileLst):
			if isPong(threeSet) or isChow(threeSet):
				newWinCombo = winCombo + threeSet
				if len(newWinCombo) > len(curLongCombo):
					curLongCombo = newWinCombo[:]
				newTileLst = tileLst[:]
				for tile in threeSet:
					newTileLst.remove(tile)
				tmp = longestCombo(newTileLst, newWinCombo, curLongCombo)
				if len(tmp) > len(curLongCombo):
					curLongCombo = tmp
	return curLongCombo

# recursive backtracking to find the all singular tiles that could make the tileLst hand winning
def winningTiles(imageNames, hand):
	tileLst = hand.tileNames
	winningTiles = []
	for tileName in imageNames:
		newTileLst = tileLst + [tileName]
		if winningCombo(newTileLst):
			winningTiles.append(tileName)
	return winningTiles

# takes list of tile names (should be hand and meld) and returns score of the hand
def handScore(tileLst):
	handCombo = longestComboScore(tileLst)
	dragons = 0
	winds = 0
	# count winds and dragons
	if handCombo[0].count("dred.png") >= 3:
		dragons += 1
	if handCombo[0].count("dwhite.png") >= 3:
		dragons += 1
	if handCombo[0].count("dgreen.png") >= 3:
		dragons += 1
	if handCombo[0].count("weast.png") >= 3:
		winds += 1
	if handCombo[0].count("wwest.png") >= 3:
		winds += 1
	if handCombo[0].count("wnorth.png") >= 3:
		winds += 1
	if handCombo[0].count("wsouth.png") >= 3:
		winds += 1
	pts = 0
	if handCombo[1] == True and handCombo[2] == False: # 3 pts for all pong
		pts += 3
		print("All Pong +3")
	if handCombo[1] == False and handCombo[2] == True: # 1 pt for all chow
		pts += 1
		print("All Chow + 1")
	# all suit w/ honors is +3, all suits is +6
	# all bamboo
	if handCombo[3] == True and handCombo[4] == False and handCombo[5] == False:
		pts += 3
		print("All Bamboo w/ Honors +3")
		if winds == 0 and dragons == 0:
			pts += 3
			print("All Bamboo +3")
	# all dot
	if handCombo[3] == False and handCombo[4] == True and handCombo[5] == False:
		pts += 3
		print("All Dot w/ Honors +3")
		if winds == 0 and dragons == 0:
			pts += 3
			print("All Dot +3")
	# all character
	if handCombo[3] == False and handCombo[4] == False and handCombo[5] == True:
		pts += 3
		print("All Character w/ Honors +3")
		if winds == 0 and dragons == 0:
			pts += 3
			print("All Character +3")
	# point for each wind pong
	if winds > 0: 
		pts += winds
		print(str(winds) + " Winds +" + str(winds))
	# point for each dragon pong
	if dragons > 0:
		pts += dragons
		print(str(dragons) + " Dragon(s) +" + str(dragons))
	return pts


# recursion to find the longest possible combo from tileLst
# may return a winning combo if possible
def longestComboScore(tileLst, winCombo = None, curLongCombo = None, anyPong = False, anyChow = False,\
	anyBamboo = False, anyDot = False, anyCharacter = False):
	if winCombo == None:
		winCombo = []
		curLongCombo = []
		copyL = copy.copy(L)
		# get rid of flowers and seasons
		for tile in tileLst:
			if tile[0] == "f" or tile[0] == "s":
				copyL.remove(tile)
		tileLst = copyL
	#print(winCombo, "w")
	#print(curLongCombo)
	# final combo should always be a winning pair, not a meld
	if len(tileLst) == 2 and tileLst[0] == tileLst[1]:
		return (curLongCombo, anyPong, anyChow, anyBamboo, anyDot, anyCharacter)
	else:
		for threeSet in threePowerset(tileLst):
			if isPong(threeSet):
				newWinCombo = winCombo + threeSet
				if len(newWinCombo) > len(curLongCombo):
					curLongCombo = newWinCombo[:]
				newTileLst = tileLst[:]
				bmb = True
				dot = True
				chara = True
				windOrDragon = False
				for tile in threeSet:
					newTileLst.remove(tile)
				# point for dragon pong (special)
				if threeSet[0][0] == "d":
					windOrDragon = True
				# pong of wind should just change the anyWind
				if threeSet[0][0] == "w":
					windOrDragon = True
				if threeSet[0][1:] != "bamboo.png":
					bmb = False
				if threeSet[0][1:] != "dot.png":
					dot = False
				if threeSet[0][1:] != "character.png":
					chara = False
				# okay to have honors and still be all of one suit, keep status quo
				if windOrDragon == True:
					tmp = longestComboScore(newTileLst, newWinCombo, curLongCombo, True, anyChow,\
					anyBamboo, anyDot, anyCharacter)
				else:
					tmp = longestComboScore(newTileLst, newWinCombo, curLongCombo, True, anyChow,\
						anyBamboo or bmb, anyDot or dot, anyCharacter or chara)
				if len(tmp[0]) > len(curLongCombo):
					curLongCombo = tmp[0]
					anyPong = tmp[1]
					anyChow = tmp[2]
					anyBamboo = tmp[3]
					anyDot = tmp[4]
					anyCharacter = tmp[5]
			elif isChow(threeSet):
				newWinCombo = winCombo + threeSet
				if len(newWinCombo) > len(curLongCombo):
					curLongCombo = newWinCombo[:]
				newTileLst = tileLst[:]
				bmb = True
				dot = True
				chara = True
				for tile in threeSet:
					newTileLst.remove(tile)
				if threeSet[0][1:] != "bamboo.png":
					bmb = False
				if threeSet[0][1:] != "dot.png":
					dot = False
				if threeSet[0][1:] != "character.png":
					chara = False
				tmp = longestComboScore(newTileLst, newWinCombo, curLongCombo, anyPong, True,\
					anyBamboo or bmb, anyDot or dot, anyCharacter or chara)
				if len(tmp[0]) > len(curLongCombo):
					curLongCombo = tmp[0]
					anyPong = tmp[1]
					anyChow = tmp[2]
					anyBamboo = tmp[3]
					anyDot = tmp[4]
					anyCharacter = tmp[5]
	return (curLongCombo, anyPong, anyChow, anyBamboo, anyDot, anyCharacter)

L = ['f4.png', 's1.png', '2dot.png', '3dot.png', '4dot.png', '8dot.png', '6dot.png', '7dot.png', '6dot.png', '4dot.png', '5dot.png', '7dot.png', '7dot.png', 'dgreen.png', 'dgreen.png', 'dgreen.png']
#print(longestComboScore(L), "LCS")
#print(handScore(L))


# testing / debugging
L = ['4dot.png', '9bamboo.png', '7bamboo.png', '4dot.png','8character.png','7character.png', \
'9dot.png', '6character.png','8bamboo.png']
#print(longestCombo(L))
for item in longestCombo(L):
	L.remove(item)
#print(L)
R = ['8character.png','9bamboo.png', '7bamboo.png', '8bamboo.png']
#print(winningTiles(R))

#print(threePowerset(["1bamboo", "4bamboo", "2bamboo", "1dot", "7dot","7dot", "7dot", "3bamboo", "7dot"]))
testPongChow = ["3bamboo", "1bamboo", "2bamboo"]
assert(isPong(testPongChow) == False)
assert(isChow(testPongChow) == True)
testPongChow2 = ["3dot", "3dot", "3dot"]
assert(isPong(testPongChow2) == True)
assert(isChow(testPongChow2) == False)
testKong = ["3dot", "3dot", "3dot", "3dot"]
assert(isKong(testKong) == True)
testKong2 = ["3dot", "3dot", "3dot", "5dot"]
assert(isKong(testKong2) == False)

testMelds = ["1bamboo", "4bamboo", "2bamboo", "1dot", "7dot","7dot", "7dot", "3bamboo", "7dot"]
#print(possibleMelds(testMelds))


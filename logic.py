# logic.py contains methods evaluating melds, legality, finding combos

# returns if a list of three tiles is a Pong
def isPong(lst):
	if len(lst) != 3: # pong is 3 elements
		return False
	# all elements must be the same 
	elif lst[0] == lst[1] and lst[1] == lst[2]: 
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
def handScore(data, tileLst):
	scoreText = ""
	copyLst = copy.copy(tileLst)
	handCombo = longestComboScore(copyLst)
	longComboLen = len(handCombo[0])
	pts = 0
	flowSea = 0
	for tile in tileLst:
		if tile[0] == "f" or tile[0] == "s":
			if int(tile[1]) == data.turnInd + 1: # flowers and season start at 1 not 0
				flowSea += 1
	if flowSea >= 1:
		scoreText += str(flowSea) + "Flower/Season(s) of Own Wind +" + str(flowSea) + "\n"
		pts += flowSea
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
	if handCombo[1] == True and handCombo[2] == False: # 3 pts for all pong
		pts += 3
		scoreText += "All Pong +3\n"
	if handCombo[1] == False and handCombo[2] == True: # 1 pt for all chow
		pts += 1
		scoreText += "All Chow +1\n"
	# all suit w/ honors is +3, all suits is +6
	# all bamboo
	if handCombo[3] == True and handCombo[4] == False and handCombo[5] == False:
		pts += 3
		scoreText += "All Bamboo w/ Honors +3\n"
		if winds == 0 and dragons == 0:
			pts += 3
			scoreText += "All Bamboo +3\n"
	# all dot
	if handCombo[3] == False and handCombo[4] == True and handCombo[5] == False:
		pts += 3
		scoreText += "All Dot w/ Honors +3\n"
		if winds == 0 and dragons == 0:
			pts += 3
			scoreText += "All Dot +3\n"
	# all character
	if handCombo[3] == False and handCombo[4] == False and handCombo[5] == True:
		pts += 3
		scoreText += "All Character w/ Honors +3\n"
		if winds == 0 and dragons == 0:
			pts += 3
			scoreText += "All Character +3\n"
	# point for each wind pong
	if winds > 0: 
		pts += winds
		scoreText += str(winds) + " Winds +" + str(winds) + "\n"
	# point for each dragon pong
	if dragons > 0:
		pts += dragons
		scoreText += str(dragons) + " Dragon(s) +" + str(dragons) + "\n"
	return [pts, scoreText, longComboLen]


# recursion to find the longest possible combo from tileLst
# may return a winning combo if possible
def longestComboScore(tileLst, winCombo = None, curLongCombo = None, anyPong = False, anyChow = False,\
	anyBamboo = False, anyDot = False, anyCharacter = False):
	if winCombo == None:
		winCombo = []
		curLongCombo = []
		copyL = copy.copy(tileLst)
		# get rid of flowers and seasons
		for tile in tileLst:
			if tile[0] == "f" or tile[0] == "s":
				copyL.remove(tile)
		tileLst = copyL
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

# returns a heuristic value based on potential winning hand score 
# and how close you are to attaining that hand score
# tileLst is the names of both the tiles in hand and melds
# hand loses value if the removed tile is similar to other tiles
def handHeuristic(data, tileLst, removedTile):
	copyLst = copy.copy(tileLst)
	hs = handScore(data, copyLst)
	pts = hs[0]
	longComboLen = hs[2]
	similarityRate = 1 # less is more similar
	# if you needed one more tile to pong it
	if tileLst.count(removedTile) >= 1:
		similarityRate *= 0.5
	if removedTile[0] in "123456789":
		# if you needed one more tile to chow it
		if str(int(removedTile[0]) + 1) + removedTile[1:] in tileLst\
		or str(int(removedTile[0]) - 1) + removedTile[1:] in tileLst:
			similarityRate *= 0.75
		# if you needed one more tile to chow it but it's farther away
		if str(int(removedTile[0]) + 2) + removedTile[1:] in tileLst\
		or str(int(removedTile[0]) - 2) + removedTile[1:] in tileLst:
			similarityRate *= 0.85
	# add 1 because 0 "potential" hand can still get to above 0 in score  by self-pick
	# multiply for tilesFromWin because it matters more than pts
	heurVal = (pts + 1) * ((longComboLen + 1) * 2) * similarityRate
	return heurVal

# returns a list of a maximum of 2 tiles that are optimal based on handHeuristic()
def discAI(data):
    curL = copy.copy(data.turnOrder[data.turnInd].tileNames)
    maxHeurVal = 0
    maxHeurValInd = [0]
    i = 0
    for tile in data.turnOrder[data.turnInd].tileNames:
        removedTile = tile
        curL.remove(removedTile)
        heurVal = handHeuristic(data, curL, removedTile)
        curL.append(removedTile)
        if heurVal > maxHeurVal:
            maxHeurValInd = [i]
            maxHeurVal = heurVal
        # maximum of 2 recommendations
        elif heurVal == maxHeurVal and len(maxHeurValInd) <= 1:
        	maxHeurValInd.append(i)
        i += 1
    bestRemove = []
    for ind in maxHeurValInd:
    	bestRemove.append(data.turnOrder[data.turnInd].tileNames[ind])
    return bestRemove

# cpuTiles is only a tile from those that are not melded
def discAIEasy(data):
	cpuTiles = copy.copy(data.turnOrder[data.turnInd].tileNames)
	meldTiles = longestCombo(cpuTiles)
	for tile in meldTiles:
		cpuTiles.remove(tile)
	return cpuTiles

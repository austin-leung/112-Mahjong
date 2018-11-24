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
def checkMelds(tileLst):
	solutionLst = []
	trios = threePowerset(tileLst)[0]
	quads = threePowerset(tileLst)[1]
	for trio in trios:
		if isChow(trio):
			trio.append("Chow")
			solutionLst.append(sorted(trio))
		elif isPong(trio):
			trio.append("Pong")
			solutionLst.append(trio)
	for quad in quads:
		if isKong(quad):
			trio.append("Kong")
			solutionLst.append(quad)
	return solutionLst

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
def threePowerset(tileLst):
 	psets = powerset(tileLst)
 	threeLst = []
 	fourLst = []
 	for lst in psets:
 		if len(lst) == 3:
 			threeLst.append(lst)
 		if len(lst) == 4:
 			fourLst.append(lst)
 	return [threeLst, fourLst]
"""
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
print(checkMelds(testMelds))
"""


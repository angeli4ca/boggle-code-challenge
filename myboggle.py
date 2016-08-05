import collections
import random
import string


def loadDictionary(fileName):
	wordDictionary = collections.defaultdict(list)
	with open(fileName) as f:
		for w in f.readlines():
			if len(w) > 3:
				wordDictionary[w[0]].append(w.strip())
	return wordDictionary
	
	
def getRandomGrid(n):
	grid = [[random.choice(string.ascii_uppercase) for column in range(n)] for row in range(n)]
	return grid

def printGrid(grid):
	for x in grid: 
		print x
		
def getAdjacentLetters(grid, r, c):
	gridSize = len(grid)
	neighbors = [ [(r-1,c-1),(r-1,c),(r-1,c+1)],
				   [(r,c-1),          (r,c+1)],
				   [(r+1,c-1),(r+1,c) ,(r+1,c+1)] ]

	# if on the edge of grid (column)
	if c == 0:
		res = [n[1:] for n in neighbors]
	elif c == gridSize-1:
		res = [neighbors[0][0:2], [neighbors[1][0]], neighbors[2][0:2]]
	else:
		res = neighbors
		
	# if on the edge of grid (row)
	if r == 0:
		res = res[1:]
	elif r == gridSize-1:
		res = res[0:2]
	else:
		pass
	
	letters = []
	for row in res:
		letters.extend( [(grid[r][c],r,c) for r,c in row] )

	return letters

def getPrefixMatches(word, dictionary):
	return [m for m in dictionary[word[0]] if m.startswith(word)]	

def isValidWord(word,dictionary):
	return word in dictionary[word[0]]

def getWords(grid,dictionary,seed_letter):

	# nested recursive function
	def genCandidates(results, seed_letter, ignored, curWord=""):			
	
		
		
		if isValidWord(curWord,dictionary):
			results.add(curWord)
			
		
		# make sure we dont visit the same letter twice
		ignored.add(seed_letter)
	
		neighbors = getAdjacentLetters(grid,seed_letter[1],seed_letter[2])
		
		# remove cells we have visited before by checking against the ignored list
		candidates = [n for n in neighbors if n not in ignored]
		
		# see how many words we can find for each candidate prefix
		num_matches = [len(getPrefixMatches(curWord + n[0], dictionary)) for n in candidates]
		
		# zip them together in a convenient list of tuples
		matches = zip(candidates,num_matches)
		
		# for each candidate with more than 0 matches recursively call the function
		for c,numMatches in matches:
			if numMatches > 0:
				genCandidates(results,c,ignored,curWord=curWord + c[0])
	

	# a set to keep track of the results
	results = set()
	
	# start the recursion
	genCandidates(results,seed_letter,set(),curWord=seed_letter[0])



	return results

def solveBoggle(dict, grid, seeds):
	totResults = set()
	for seed in seeds:			
		results = getWords(grid,dictionary,seed)
		totResults = totResults.union(results)
	return totResults				

if __name__ == '__main__':
#add exception handling
	dictionary = loadDictionary('scrabble-dictionary.txt')
	n = input("Please, enter the number of tiles in a row/column: ")
	if n <= 0:
		n = input(“Incorrect input. Please, enter the number greater that 0")
	#n = 0
	grid = getRandomGrid(n)
	printGrid(grid)
	print "Processing... "
	seeds = []
	for r, row in enumerate(grid):
		for c, letter in enumerate(row):
			seeds.append((letter, r, c))
			
	results = solveBoggle(dictionary, grid, seeds)	
	print "%s words were found:" % len(results)
	print ", ".join(sorted(results))
		
	
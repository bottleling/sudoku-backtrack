import math
import time
import copy
import random

class Node:
	def __init__(self, value, domain):
		self.value = value;
		self.domain = domain;
	def __repr__(self):
		return "Node (%s , %s)" %(self.value, str(self.domain))

class Puzzle:
	def __init__(self,filename):
		self.puzzle = [[Node(None,[1,2,3,4,5,6,7,8,9]) for i in range(9)] for j in range(9)]
		self.readFile(filename)
		self.alterAllDomains(self.puzzle)
	def getDomain(self,x,y):
		return self.puzzle[x][y].domain
	def removeFromDomain(self,x,y,valToRemove):
		if valToRemove in self.puzzle[x][y].domain:
			self.puzzle[x][y].domain.remove(valToRemove)
	def readFile(self, filename):
		with open(filename, 'r') as f:
			for i in range(9):
				line = f.readline()
				for j in range(9):
					try:
						self.puzzle[i][j].value = int(line[j])
						self.puzzle[i][j].domain = []
					except:
						continue

	def hasConflict(self,rowIndex, colIndex):
		val = self.puzzle[rowIndex][colIndex].value
		#Check no value in this row has the same value as this assignment:
		for j in range(0,9):
			if j != colIndex:
				if self.puzzle[rowIndex][j].value == val:
					return True

		#Check no value in this column has the same value as this assignment:
		for i in range(0,9):
			if i != rowIndex:
				if self.puzzle[i][colIndex].value == val:
					return True

		#Check no value in this subsquare has the same value as this assignment:
		boxR = int (math.floor(rowIndex/3) * 3 ) #row0-1's box will begin at row 0, row 3-5's box will begin at row 3. row 6-8's box will begin at row 6
		boxC = int( math.floor(colIndex/3) * 3 ) #col0-1's box will begin at col 1...
		for i in range(boxR, boxR+3): #check each row of the box
			for j in range(boxC,boxC+3): #check each col of the box
				if i == rowIndex and j == colIndex:
					continue
				else:
					if self.puzzle[i][j].value == val:
						return True

		return False
	
	def isComplete(self):
		for i in range(9):
			for j in range(9):
				if self.puzzle[i][j].value == None:
					return False
		return True
	
	def alterAllDomains(self , grid):
		values = set()
		for i in range(0,9):
			for j in range(0,9):
				values.add(grid[i][j].value)
			for j in range(0,9):
				for x in values:
					self.removeFromDomain(i,j,x)
			values.clear()

		for j in range(0,9):
			for i in range(0,9):
				values.add(grid[i][j].value)
			for i in range(0,9):
				for x in values:
					self.removeFromDomain(i,j,x)
			values.clear()

		for i in range(0,9,3):
			for j in range(0,9,3):
				boxR = int (math.floor(i/3) * 3 ) #row0-1's box will begin at row 0, row 3-5's box will begin at row 3. row 6-8's box will begin at row 6
				boxC = int( math.floor(j/3) * 3 ) #col0-1's box will begin at col 1...
				for i in range(boxR, boxR+3): #check each row of the box
					for j in range(boxC,boxC+3): #check each col of the box
						values.add(grid[i][j].value)
				#print "boxR:",boxR, " boxC:", boxC, values
				for m in range(boxR,boxR+3):
					for n in range(boxC,boxC+3):
						for x in values:
							self.removeFromDomain(m,n,x)
				values.clear()

	def getMostConstrainedCoordinates(self): #unassigned variable with least number of values in its domain
		coords=[]
		size = 0
		for i in range(9):
			for j in range(9):
				if self.puzzle[i][j].value == None:
					if len(coords) == 0:
						coords.append((i,j))
						size = len(self.getDomain(i,j))
					if len(self.getDomain(i,j))  == size:
						coords.append((i,j))
					if len(self.getDomain(i,j))  < size:
						del coords[:]
						size = len(self.getDomain(i,j))
						coords.append((i,j))							

		return coords #returns [(x,y),(x1,y1)...] if there are multiple unassigned nodes with the least number of values in their domain

	def getLeastConstrainedValue(self, rowIndex, colIndex):
		domain = self.getDomain(rowIndex,colIndex)
		if len (domain) ==1:
			return domain
		lc = []
		for x in range(len(domain)):
			count = 0 #counts the number of variables with domains containing this value (ie if assigned, these domains will all be altered)
			v = domain[x]
			for j in range(0,9):
				if j != colIndex:
					if v in self.getDomain(rowIndex,j):
						count +=1
			for i in range(0,9):
				if i != rowIndex:
					if v in self.getDomain(i,colIndex):
						count +=1

			boxR = int (math.floor(rowIndex/3) * 3 ) #row0-1's box will begin at row 0, row 3-5's box will begin at row 3. row 6-8's box will begin at row 6
			boxC = int( math.floor(colIndex/3) * 3 ) #col0-1's box will begin at col 1...
			for i in range(boxR, boxR+3): #check each row of the box
				for j in range(boxC,boxC+3): #check each col of the box
					if i == rowIndex and j == colIndex:
						continue
					else:
						if v in self.getDomain(i,j):
							count +=1
			lc.append(count)

		return [d for (lc,d) in sorted(zip(lc,domain))]

	def __repr__(self):
		str= ""
		
		for i in range(9):
			s = ""
			for j in range(9):
				s+= "%5s " % self.puzzle[i][j].value
			s += "\n --------- \n"
			str+=s
		return str
		

def backtrack(grid):
	if grid.isComplete():
		return True
	mostConstrainedCoords = grid.getMostConstrainedCoordinates()
	if len(mostConstrainedCoords) >1:
		random.shuffle(mostConstrainedCoords)
	x,y= mostConstrainedCoords[0]
	for d in grid.getLeastConstrainedValue(x,y):
		puzzle = grid.puzzle
		puzzle[x][y].value = d
		if not grid.hasConflict(x,y):
			grid.removeFromDomain(x,y,d)
			puzzleCopy = copy.deepcopy(puzzle)
			grid.alterAllDomains(puzzle)
			if backtrack(grid): #if the path from this value fails, go to the next least constrained value
				return True
			else:
				grid.puzzle = puzzleCopy
		else:
			puzzle[x][y].value = None #remove var=value from assignement 
	return False

verbose = True #True(1): display result of sudoku board; False(0): not display sudoku result board
runs = 1	#it can set to any numerical value, in this case, each sudoku level only run one time
files = ["test/sudoku_easy.txt", "test/sudoku_medium.txt", "test/sudoku_hard.txt", "test/sudoku_hardest.txt"]
print "Parameters- Verbose: %s , Runs: %d" %(verbose, runs)
for f in files:
	correct =0.0
	times=0
	for i in range(0,runs):
		p = Puzzle(f)
		t = time.time()
		result = backtrack(p)
		times += time.time() -t
		if result:
			correct +=1
		if verbose:
			print p
	print "File: %s Proportion successful: %f Avg time: %f" %(f,correct/runs,times/runs)

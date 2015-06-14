class Node:
	def __init__(self, value, domain=[1,2,3,4,5,6,7,8,9]):
		self.value = value;
		self.domain = domain;
	def __repr__(self):
		return "Node (%s , %s)" %(self.value, str(self.domain))

class Puzzle:
	def __init__(self,filename):
		self.puzzle = [[Node(None) for i in range(9)] for j in range(9)]
		self.readFile(filename)
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

	def hasConflict(rowIndex, colIndex):
		#Check alldiff in row:
			priorValue = puzzle[rowIndex][0].value
			for j in range(1,10):
				if puzzle[rowIndex][j].value == priorValue:
					return True
				else:
					priorValue = puzzle[rowIndex][j].value

		#Check alldiff in col:
			priorValue = puzzle[0][colIndex].value
			for i in range(1,10):
				if puzzle[i][colIndex].value == priorValue:
					return True
				else:
					priorValue = puzzle[i][colIndex].value

		#Check alldiff in subsquare
			boxR = math.floor(rowIndex/3) * 3 #row 5's box will begin at row 3


p = Puzzle("test/sudoku_easy.txt")
print p.puzzle
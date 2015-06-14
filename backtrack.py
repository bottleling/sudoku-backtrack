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
		val = self.puzzle[rowIndex][colIndex].value()
		#Check no value in this row has the same value as this assignment:
			for j in range(0,9):
				if j != colIndex:
					if self.puzzle[rowIndex][j].value == val:
						return True

		#Check no value in this column has the same value as this assignment:
			for i in range(1,10):
				if i != rowIndex:
					if self.puzzle[i][colIndex].value == val:
						return True

		#Check no value in this subsquare has the same value as this assignment:
			boxR = math.floor(rowIndex/3) * 3 #row0-1's box will begin at row 0, row 3-5's box will begin at row 3. row 6-8's box will begin at row 6
			boxC = math.floor(colIndex/3) * 3 #col0-1's box will begin at col 1...
			for i in range(boxR, boxR+3): #check each row of the box
				for j in range(boxC,boxC+3): #check each col of the box
					if i == rowIndex and j == colIndex:
						continue
					else:
						if self.puzzle[i][j].value == val:
							return True

			return False



p = Puzzle("test/sudoku_easy.txt")
print p.puzzle
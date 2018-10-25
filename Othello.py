#Library imports
from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy

#Initialization of Constants
WIDTH = 500
HEIGHT = 600
GREEN = "green"
WHITE = "white"
BLACK = "black"
RED = "red"
PLAYER1 = "w"
PLAYER2 = "b"
player = 0
passed1 = False
AI = 1
switched = False


#Player 0 is black
#Player 1 is White


#Initialization of Variables
nodes = 0
depth = 4
moves = 0

#Tkinter setup, which sets up the GUI for the program.
root = Tk()
screen = Canvas(root, width=WIDTH, height=HEIGHT, background=GREEN,highlightthickness=0)
screen.pack()

class Board:
	def __init__(self):
		global player
		global PLAYER1
		global PLAYER2
		global passed1

		self.player = 0
		#Black Goes First(0 is Black and the Human, 1 is white and the computer)
		self.passed = False
		self.won = False

		#Initializing an empty board
		self.array = []
		for x in range(8):
			self.array.append([])
			for y in range(8):
				self.array[x].append(None)

		#Initializing center values
		self.array[3][3]=PLAYER1
		self.array[3][4]=PLAYER2
		self.array[4][3]=PLAYER2
		self.array[4][4]=PLAYER1

		#Initializing old values
		self.oldarray = self.array
	#Updating the board to the screen
	def update(self):
		global player
		global PLAYER1
		global PLAYER2
		global WHITE
		global BLACK
		global AI


		screen.delete("highlight")
		screen.delete("tile")
		for x in range(8):
			for y in range(8):
				#Draws white pieces
				if self.oldarray[x][y]==PLAYER1: #w
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")
				#Draws  Black pieces
				elif self.oldarray[x][y]==PLAYER2:
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		#Animates the new pieces
		screen.update()
		for x in range(8):
			for y in range(8):
				if self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]==PLAYER1:
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking animation
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.005)
						screen.update()
						screen.delete("animated")
					#Growing animation
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.005)
						screen.update()
						screen.delete("animated")
					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
					screen.update()

				elif self.array[x][y]!=self.oldarray[x][y] and self.array[x][y]==PLAYER2:
					screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking animation
					for i in range(21):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.005)
						screen.update()
						screen.delete("animated")
					#Growing animation
					for i in reversed(range(21)):
						screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.005)
						screen.update()
						screen.delete("animated")

					screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
					screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
					screen.update()

		#Drawing the circle for potential moves, the circles have a white outline and a black fill color.
		for x in range(8):
			for y in range(8):
				if self.player == player:
					#evaluates the potential moves to see which are valid plays
					if valid(self.array,self.player,x,y):
						screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill=BLACK,outline=WHITE)

			#as long as the game is not over the scoreboard will be drawn on the screen
		if not self.won:
			#Draws the scoreboard and updates the screen
			self.drawScoreBoard()
			screen.update()

			#If the computer is AI, make a move (Game could be modified to be two humans later)
			if self.player==AI:
				Start = time()
				self.oldarray = self.array
				alphaBeta = self.alphaBeta(self.array,depth,-float("inf"),float("inf"),AI)
				self.array = alphaBeta[1]

				if len(alphaBeta)==3:
					position = alphaBeta[2]
					self.oldarray[position[0]][position[1]]=PLAYER1

				self.player = 1-self.player
				deltaTime = round((time()-Start)*100)/100
				if deltaTime<2:
					sleep(2-deltaTime)
				nodes = 0
				#Checks to see if the player must pass their move or not.
				self.passTest()
		else:
			screen.create_text(250,550,anchor="c",font=("Times New Roman",15), text="Game Completed!")

	#Moves to position that is specified by the user input (I.E a click) and updates the screen
	def boardMove(self,x,y):
		global player, PLAYER1, PLAYER2

		if player == 1:
			color = PLAYER1
		else:
			color = PLAYER2

		#Makes the Move and updates screen
		self.oldarray = self.array
		self.oldarray[x][y]=color
		self.array = move(self.array,x,y)

		#Switch Player
		self.player = 1-self.player
		self.update()

		#Check if AI must pass move
		self.passTest()
		self.update()

	# function that draws the scoreboard to the scrreen
	def drawScoreBoard(self):
		global player
		global PLAYER1
		global PLAYER2
		global WHITE
		global BLACK
		#Removes the old score
		screen.delete("score")

		#Keeps track of the score by the number of spaces occupied
		player_score = 0
		computer_score = 0

		#cycles through the array and counts the number of white spaces and black spaces
		for x in range(8):
			for y in range(8):
				if self.array[x][y]==PLAYER2:
					player_score+=1
				elif self.array[x][y]==PLAYER1:
					computer_score+=1

		#Marker that shows who's turn it is, if it is the players turn, a black circle is on the screen next to their score.
		#If it is the AI's turn, then there is a black circle next to the AI's score.  When it is the other person's turn a
		#circle that is the same color is the background is displayed, (mimicking like there is none there.)
		if self.player==0:
			player_color = BLACK
			computer_color = GREEN
		else:
			player_color = GREEN
			computer_color = BLACK

		screen.create_oval(5,540,25,560,fill=player_color,outline=player_color)
		screen.create_oval(380,540,400,560,fill=computer_color,outline=computer_color)

		#Pushing text to screen
		screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=player_score) #Human
		screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=computer_score) #AI

		moves = player_score+computer_score

	#Test if player must pass: if they do, switch the player (so that the track is ok)
	def passTest(self):

		mustPass = True
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					mustPass = False
		if mustPass:
			self.player = 1-self.player
			if self.passed==True:
				self.won = True
			else:
				self.passed = True
			self.update()
		else:
			self.passed = False

	#This contains the minimax algorithm
	#based off the pseudocode at http://en.wikipedia.org/wiki/Minimax
	def minimax(self, node, depth, maximizing):
		global nodes
		nodes += 1
		boards = []
		choices = []

		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([SEF3(node,1-maximizing),node])

		if maximizing:
			bestValue = -float("inf")
			bestBoard = ()
			for board in boards:
				val = self.minimax(board,depth-1,0)[0]
				if val>bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

		else:
			bestValue = float("inf")
			bestBoard = ()
			for board in boards:
				val = self.minimax(board,depth-1,1)[0]
				if val<bestValue:
					bestValue = val
					bestBoard = board
			return ([bestValue,bestBoard])

	#alphaBeta pruning on the minimax tree
	#based on the pseudocode at: http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
	def alphaBeta(self,node,depth,alpha,beta,maximizing):
		global nodes
		nodes += 1
		boards = []
		choices = []
		for x in range(8):
			for y in range(8):
				if valid(self.array,self.player,x,y):
					test = move(node,x,y)
					boards.append(test)
					choices.append([x,y])

		if depth==0 or len(choices)==0:
			return ([SEFControl(node,maximizing),node])

		if maximizing:
			v = -float("inf")
			bestBoard = []
			bestChoice = []
			for board in boards:
				boardValue = self.alphaBeta(board,depth-1,alpha,beta,0)[0]
				if boardValue>v:
					v = boardValue
					bestBoard = board
					bestChoice = choices[boards.index(board)]
				alpha = max(alpha,v)
				if beta <= alpha:
					break
			return([v,bestBoard,bestChoice])
		else:
			v = float("inf")
			bestBoard = []
			bestChoice = []
			for board in boards:
				boardValue = self.alphaBeta(board,depth-1,alpha,beta,1)[0]
				if boardValue<v:
					v = boardValue
					bestBoard = board
					bestChoice = choices[boards.index(board)]
				beta = min(beta,v)
				if beta<=alpha:
					break
			return([v,bestBoard,bestChoice])

#Returns a board after making a move
#Assumes the move is valid
def move(passedArray,x,y):
	global PLAYER1
	global PLAYER2
	#Must copy the passedArray so we don't alter the original
	array = deepcopy(passedArray)
	#Set color and set the moved location to be that color
	if board.player==0:
		color = PLAYER2
	else:
		color=PLAYER1
	array[x][y]=color

	#Determining the neighbours to the square
	neighbours = []
	for i in range(max(0,x-1),min(x+2,8)):
		for j in range(max(0,y-1),min(y+2,8)):
			if array[i][j]!=None:
				neighbours.append([i,j])

	#Which tiles to convert
	convert = []

	#For all the generated neighbours, determine if they form a line
	#If a line is formed, we will add it to the convert array
	for neighbour in neighbours:
		neighX = neighbour[0]
		neighY = neighbour[1]
		#Check if the neighbour is of a different color - it must be to form a line
		if array[neighX][neighY]!=color:
			#The path of each individual line
			path = []

			#Determining direction to move
			deltaX = neighX-x
			deltaY = neighY-y

			tempX = neighX
			tempY = neighY

			#While we are in the bounds of the board
			while 0<=tempX<=7 and 0<=tempY<=7:
				path.append([tempX,tempY])
				value = array[tempX][tempY]
				#If we reach a blank tile, we're done and there's no line
				if value==None:
					break
				#If we reach a tile of the player's color, a line is formed
				if value==color:
					#Append all of our path nodes to the convert array
					for node in path:
						convert.append(node)
					break
				#Move the tile
				tempX+=deltaX
				tempY+=deltaY

	#Convert all the appropriate tiles
	for node in convert:
		array[node[0]][node[1]]=color

	return array

#Method for drawing the gridlines, can change outline to false if we do not want an outline on the board.
def drawGridBackground(outline=True):

	if outline:
		screen.create_rectangle(50,50,450,450,outline="#111")

	#Draws the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal lines
		screen.create_line(50,lineShift,450,lineShift,fill="#111")

		#Vertical lines
		screen.create_line(lineShift,50,lineShift,450,fill="#111")

	screen.update()

#Simple heuristic. Compares number of each tile.
def SEF1(array,player):
	score = 0
	#Set player and opponent colors
	if player==1:
		color=PLAYER1
		opponent=PLAYER2
	else:
		color = PLAYER2
		opponent = PLAYER1
	#+1 if it's player color, -1 if it's opponent color
	for x in range(8):
		for y in range(8):
			if array[x][y]==color:
				score+=1
			elif array[x][y]==opponent:
				score-=1
	return score

#Heuristic that Weights corners and edges as more
def SEF2(array,player):
	score = 0

	#Set player and opponent colors
	if player==1:
		color=PLAYER1
		opponent=PLAYER2
	else:
		color = PLAYER2
		opponent = PLAYER1
	#Go through all the tiles
	for x in range(8):
		for y in range(8):
			#Normal tiles worth 1
			add = 1
			#Edge tiles worth 5
			if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=5
			#Corner tiles worth 1000
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = 1000
			#Add or subtract the value of the tile corresponding to the color
			if array[x][y]==color:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

#Heuristic that weights corner tiles and edge tiles as positive, adjacent to corners (if the corner is not yours) as negative
#Weights other tiles as one point
def SEF3(array,player):
	score = 0
	cornerValue = 1000 
	adjacentValue = 900 
	sideValue = 4 

	#Set player and opponent colors
	if player==AI:
		color=PLAYER1
		opponent=PLAYER2
	else:
		color = PLAYER2
		opponent = PLAYER1
	#Go through all the tiles
	for x in range(8):
		for y in range(8):
			#Normal tiles worth 1
			add = 1

			#Adjacent to corners are worth -900
			if (x==0 and y==1) or (x==1 and 0<=y<=1):
				if array[0][0]==color:
					add = sideValue #+
				else:
					add = -adjacentValue #-


			elif (x==0 and y==6) or (x==1 and 6<=y<=7):
				if array[7][0]==color:
					add = sideValue
				else:
					add = -adjacentValue

			elif (x==7 and y==1) or (x==6 and 0<=y<=1):
				if array[0][7]==color:
					add = sideValue
				else:
					add = -adjacentValue

			elif (x==7 and y==6) or (x==6 and 6<=y<=7):
				if array[7][7]==color:
					add = sideValue
				else:
					add = -adjacentValue


			#Edge tiles worth 4
			elif (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
				add=sideValue
			#Corner tiles worth 1000
			elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
				add = cornerValue
			#Add or subtract the value of the tile corresponding to the color
			if array[x][y]==color:
				score+=add
			elif array[x][y]==opponent:
				score-=add
	return score

#Seperating the use of heuristics for early/mid/late game.
def SEFControl(array,player):
	if moves<=8: 
		numMoves = 0
		for x in range(8):
			for y in range(8):
				if valid(array,player,x,y):
					numMoves += 1
		return numMoves+SEF3(array,player)
	elif moves<=52: 
		return SEF3(array,player)
	elif moves<=58: 
		return SEF2(array,player)
	else:
		return SEF2(array,player)

#Checks if a move is valid for a given array.
def valid(array,player,x,y):
	global PLAYER1
	global PLAYER2
	#Sets player color
	if player==0:
		color=PLAYER2
	else:
		color=PLAYER1

	#If there's already a piece there, it's an invalid move
	if array[x][y]!=None:
		return False

	else:
		#Generating the list of neighbours
		neighbour = False
		neighbours = []
		for i in range(max(0,x-1),min(x+2,8)):
			for j in range(max(0,y-1),min(y+2,8)):
				if array[i][j]!=None:
					neighbour=True
					neighbours.append([i,j])
		#If there's no neighbours, it's an invalid move
		if not neighbour:
			return False
		else:
			#Iterating through neighbours to determine if at least one line is formed
			valid = False
			for neighbour in neighbours:

				neighX = neighbour[0]
				neighY = neighbour[1]

				#If the neighbour color is equal to your color, it doesn't form a line
				#Go onto the next neighbour
				if array[neighX][neighY]==color:
					continue
				else:
					#Determine the direction of the line
					deltaX = neighX-x
					deltaY = neighY-y
					tempX = neighX
					tempY = neighY

					while 0<=tempX<=7 and 0<=tempY<=7:
						#If an empty space, no line is formed
						if array[tempX][tempY]==None:
							break
						#If it reaches a piece of the player's color, it forms a line
						if array[tempX][tempY]==color:
							valid=True
							break
						#Move the index according to the direction of the line
						tempX+=deltaX
						tempY+=deltaY
			return valid

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
	global depth
	global player
	xMouse = event.x
	yMouse = event.y
	if running:
		#Is it the player's turn?
		if board.player==player:
			#Delete the highlights
			x = int((event.x-50)/50)
			y = int((event.y-50)/50)
			#Determine the grid index for where the mouse was clicked

			#If the click is inside the bounds and the move is valid, move to that location
			if 0<=x<=7 and 0<=y<=7:
				if valid(board.array,board.player,x,y):
					board.boardMove(x,y)
	else:
		#Checks to see which difficulty the user selects.
		if 300<=yMouse<=350:
			#One star
			if 25<=xMouse<=155:
				depth = 2
				playGame()
			#Two star
			elif 180<=xMouse<=310:
				depth = 4
				playGame()
			#Three star
			elif 335<=xMouse<=465:
				depth = 5
				playGame()
#can run the game with r and quit the game with q.
def keyHandle(event):
	global player, passed1, AI
	symbol = event.keysym
	if symbol.lower()=="r":
		playGame()
	elif symbol.lower()=="q":
		root.destroy()
	elif symbol.lower() =="s":
		player = 1
		AI = 0
		passed1 = True
		print ("Colors changed")

def runGame():
	global running
	running = False
	#Title and shadow
	screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
	screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")

	#Creating the difficulty buttons
	for i in range(3):
		#Background
		screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
		screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

		spacing = 130/(i+2)
		for x in range(i+1):
			#Star with double shadow
			screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="\u2605", font=("Consolas", 25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
			screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")

	screen.update()

def playGame():
	global board, running
	running = True
	screen.delete(ALL)
	board = 0

	#Draw the background
	drawGridBackground()

	#Create the board and update it
	board = Board()
	board.update()

runGame()

#Binding, setting
screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
root.wm_title("Othello")
root.mainloop()

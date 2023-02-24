import random
import time
import pygame
import math

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]
		
		print("EVAL: " + str(self.eval(env)))

	def eval(self, env):
		my_fours = self.checkForStreak(env.board, env.turnPlayer.position, 3)
		my_threes = self.checkForStreak(env.board, env.turnPlayer.position, 2)
		my_twos = self.checkForStreak(env.board, env.turnPlayer.position, 1)
		comp_fours = self.checkForStreak(env.board, env.turnPlayer.opponent.position, 3)
		comp_threes = self.checkForStreak(env.board, env.turnPlayer.opponent.position, 2)
		comp_twos = self.checkForStreak(env.board, env.turnPlayer.opponent.position, 1)
		return (my_fours * 10 + my_threes * 5 + my_twos * 2) - (comp_fours * 10 + comp_threes * 5 + comp_twos * 2)

	def checkForStreak(self, board, player, streak):
		count = 0
		for i in range(6):
			for j in range(7):
				if board[i][j] == player:
					count += self.verticalStreak(i, j, board, streak)
					# count += self.horizontalStreak(i, j, board, streak)
					# count += self.diagonalCheck(i, j, board, streak)
		return count

	def verticalStreak(self, row, column, state, streak):
		consecutiveCount = 0
		k = row + 1
		while (k < 6):
			if state[k][column] == state[row][column]:
				consecutiveCount += 1
			k += 1
		for i in range(row - 1, -1, -1):
			if state[i][column] == state[row][column]:
				consecutiveCount += 1
				# print("state[" + str(i) + "][" + str(column) + "] = " + str(state[i][column]) + " con count: " + str(consecutiveCount))
			else:
				break
		if consecutiveCount == streak:
			print("Found streak for " + str(streak) + " with consecutive count " + str(consecutiveCount) + " Player: " + str(state[row][column]))
			return 1
		else:
			return 0

	def horizontalStreak(self, row, column, state, streak):
		count = 0
		for j in range(column, 7):
			if state[row][j] == state[row][column]:
				count += 1
			else:
				break
		if count >= streak:
			return 1
		else:
			return 0

	def diagonalCheck(self, row, column, state, streak):
		total = 0
		count = 0
		j = column
		for i in range(row, 6):
			if j > 6:
				break
			elif state[i][j] == state[row][column]:
				count += 1
			else:
				break
			j += 1
		if count >= streak:
			total += 1
		count = 0
		j = column
		for i in range(row, -1, -1):
			if j > 6:
				break
			elif state[i][j] == state[row][column]:
				count += 1
			else:
				break
			j += 1
		if count >= streak:
			total += 1
		return total

class minimaxAI(connect4Player):

	def play(self, env, move):
		pass

	def eval(self, env):
		my_fours = self.checkForStreak(env.board, env.turnPlayer.position, 4)
		my_threes = self.checkForStreak(env.board, env.turnPlayer.position, 3)
		my_twos = self.checkForStreak(env.board, env.turnPlayer.position, 2)
		comp_fours = self.checkForStreak(env.board, env.turnPlayer.position, 4)
		comp_threes = self.checkForStreak(env.board, env.turnPlayer.position, 3)
		comp_twos = self.checkForStreak(env.board, env.turnPlayer.position, 2)
		return (my_fours * 10 + my_threes * 5 + my_twos * 2) - (comp_fours * 10 + comp_threes * 5 + comp_twos * 2)

	def checkForStreak(self, board, player, streak):
		count = 0
		for i in range(6):
			for j in range(7):
				if board[i][j] == player:
					count += self.verticalStreak(i, j, board, streak)
					count += self.horizontalStreak(i, j, board, streak)
					count += self.diagonalCheck(i, j, board, streak)
		return count

	def verticalStreak(self, row, column, state, streak):
		consecutiveCount = 0
		for i in range(row, 6):
			if state[i][column] == state[row][column]:
				consecutiveCount += 1
			else:
				break
		if consecutiveCount >= streak:
			return 1
		else:
			return 0

	def horizontalStreak(self, row, column, state, streak):
		count = 0
		for j in range(column, 7):
			if state[row][j] == state[row][column]:
				count += 1
			else:
				break
		if count >= streak:
			return 1
		else:
			return 0

	def diagonalCheck(self, row, column, state, streak):
		total = 0
		count = 0
		j = column
		for i in range(row, 6):
			if j > 6:
				break
			elif state[i][j] == state[row][column]:
				count += 1
			else:
				break
			j += 1
		if count >= streak:
			total += 1
		count = 0
		j = column
		for i in range(row, -1, -1):
			if j > 6:
				break
			elif state[i][j] == state[row][column]:
				count += 1
			else:
				break
			j += 1
		if count >= streak:
			total += 1
		return total


class alphaBetaAI(connect4Player):

	def play(self, env, move):
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)





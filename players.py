import random
import time
import pygame
import math
import sys

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

class minimaxAI(connect4Player):

	def play(self, env, move):
		v = -math.inf

		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		
		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, env.turnPlayer)
			result = self.min_val(simulated_move, env.turnPlayer.opponent, 3, 1) 
			if(result > v):
				move[:] = [play]
				v = result

	def simulateMove(self, env, column_move, player):
		env.board[env.topPosition[column_move]][column_move] = player.position
		env.topPosition[column_move] -= 1
		env.history[int(player.position) - 1].append(column_move)
		return env

	def min_val(self, env, player, target_depth, current_depth):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return 10000 * (target_depth - current_depth + 1)
		
		if(target_depth == current_depth):
			return -1 * self.eval(env.board, player)

		v = math.inf
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.max_val(simulated_move, player.opponent, target_depth, current_depth + 1)
			if(result < v):
				v = result
		
		return v

	def max_val(self, env, player, target_depth, current_depth):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return -10000 * (target_depth - current_depth + 1)

		if(target_depth == current_depth):
			return self.eval(env.board, player)

		v = -math.inf
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.min_val(simulated_move, player.opponent, target_depth, current_depth + 1)
			if(result > v):
				v = result
		
		return v

	def eval(self, board, player):
		# weights = [
		# 	[5, 10, 15, 20, 15, 10, 5],
		# 	[10, 15, 20, 25, 20, 15, 10],
		# 	[15, 20, 25, 30, 25, 20, 15],
		# 	[15, 20, 25, 30, 25, 20, 15],
		# 	[10, 15, 20, 25, 20, 15, 10],
		# 	[5, 10, 15, 20, 15, 10, 5]
		# ]
		weights = [
      [10, 15, 20, 25, 20, 15, 10],
      [15, 20, 30, 35, 30, 20, 15],
      [20, 25, 30, 40, 30, 25, 20],
      [20, 25, 30, 40, 30, 25, 20],
      [20, 25, 35, 45, 35, 25, 20],
      [15, 30, 45, 50, 45, 30, 15],
		]

		count = 0
		for row in range(6):
			for col in range(7):
				if(board[row][col] == player.position):
					count += (weights[row][col])
				elif(board[row][col] == player.opponent.position):
					count -= (weights[row][col])
		
		return count


class alphaBetaAI(connect4Player):

	def play(self, env, move):
		v = -math.inf

		possible = env.topPosition >= 0
		indices = []

		for i, p in enumerate(possible):
			if p: 
				indices.append(i)

		random.shuffle(indices)
		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, env.turnPlayer)
			simulated_move.visualize = False
			result = self.min_val(simulated_move, env.turnPlayer.opponent, 4, 1, -math.inf, math.inf) 
			if(result > v):
				move[:] = [play]
				v = result

	def simulateMove(self, env, column_move, player):
		env.board[env.topPosition[column_move]][column_move] = player.position
		env.topPosition[column_move] -= 1
		env.history[int(player.position) - 1].append(column_move)
		return env

	def min_val(self, env, player, target_depth, current_depth, alpha, beta):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return 10000 * (target_depth - current_depth + 1)
		
		if(target_depth == current_depth):
			return -1 * self.eval(env.board, player)

		v = math.inf
		possible = env.topPosition >= 0
		indices = []

		
		for i, p in enumerate(possible):
			if p: 
				indices.append(i)

		random.shuffle(indices)
		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.max_val(simulated_move, player.opponent, target_depth, current_depth + 1, alpha, beta)
			if(result < v):
				v = result

			if(v <= alpha):
				return v
			
			beta = min(beta, v)
		
		return v

	def max_val(self, env, player, target_depth, current_depth, alpha, beta):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return -10000 * (target_depth - current_depth + 1)

		if(target_depth == current_depth):
			return self.eval(env.board, player)

		v = -math.inf
		possible = env.topPosition >= 0
		indices = []

		for i, p in enumerate(possible):
			if p: 
				indices.append(i)

		random.shuffle(indices)
		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.min_val(simulated_move, player.opponent, target_depth, current_depth + 1, alpha, beta)
			if(result > v):
				v = result

			if(v >= beta):
				return v
			
			alpha = max(alpha, v)
		
		return v

	def eval(self, board, player):
		weights = [
			[5, 10, 15, 20, 15, 10, 5],
			[10, 15, 20, 25, 20, 15, 10],
			[15, 20, 25, 30, 25, 20, 15],
			[15, 20, 25, 30, 25, 20, 15],
			[10, 15, 20, 25, 20, 15, 10],
			[10, 15, 20, 25, 20, 15, 10],
		]

		count = 0
		for row in range(6):
			for col in range(7):
				if(board[row][col] == player.position):
					count += (weights[row][col])
				elif(board[row][col] == player.opponent.position):
					count -= (weights[row][col])
		
		return count
	# 	score = 0

	# 	center_array = []
	# 	for i in list(board[:, 3]):
	# 		center_array.append(i)
	# 	center_count = center_array.count(player.position)
	# 	score += center_count * 6

	# 	# vertical 
	# 	for col in range(7):
	# 		col_array = [int(i) for i in list(board[:, col])]
	# 		for row in range(3):
	# 			arr = col_array[row:row + 4]
	# 			score += self.get_score(arr, player.position, player.opponent.position)

	# 	# horizontal 
	# 	for row in range(6):
	# 		row_array = [int(i) for i in list(board[row, :])]
	# 		for col in range(4):
	# 			arr = row_array[col:col + 4]
	# 			score += self.get_score(arr, player.position, player.opponent.position)

	# 	# downward diagonal
	# 	for row in range(3):
	# 		for col in range(4):
	# 			arr = [board[row + 3 - i][col + i] for i in range(4)]
	# 			score += self.get_score(arr, player.position, player.opponent.position)

	# 	# upward diagonals
	# 	for row in range(3):
	# 		for col in range(4):
	# 			arr = [board[row + i][col + i] for i in range(4)]
	# 			score += self.get_score(arr, player.position, player.opponent.position)

	# 	return score

	# def get_score(self, arr, player, opponent):
	# 	score = 0
		
	# 	if arr.count(player) == 4:
	# 		score += 250
	# 	elif arr.count(player) == 3 and arr.count(0) == 1:
	# 		score += 25
	# 	elif arr.count(player) == 2 and arr.count(0) == 2:
	# 		score += 12

	# 	if arr.count(opponent) == 4:
	# 		score -= 250
	# 	elif arr.count(opponent) == 3 and arr.count(0) == 1:
	# 		score -= 25
	# 	elif arr.count(opponent) == 2 and arr.count(0) == 2:
	# 		score -= 12
		

	# 	return score
 

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




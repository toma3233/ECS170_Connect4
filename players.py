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
		env.history[player.position - 1].append(column_move)
		return env

	def min_val(self, env, player, target_depth, curr_depth):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return 6900 * (target_depth - curr_depth + 1)
		
		if(target_depth == curr_depth):
			return -1 * self.evaluation_func(env.board, player)

		v = math.inf
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.max_val(simulated_move, player.opponent, target_depth, curr_depth + 1)
			if(result < v):
				v = result
		
		return v

	def max_val(self, env, player, target_depth, curr_depth):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return -6900 * (target_depth - curr_depth + 1)

		if(target_depth == curr_depth):
			return self.evaluation_func(env.board, player)

		v = -math.inf
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)

		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.min_val(simulated_move, player.opponent, target_depth, curr_depth + 1)
			if(result > v):
				v = result
		
		return v

	def evaluation_func(self, board, player):
		weights = [
			[3, 6, 9, 12, 9, 6, 3],
			[6, 9, 12, 15, 12, 9, 6],
			[9, 12, 15, 18, 15, 12, 9],
			[9, 12, 15, 18, 15, 12, 9],
			[6, 9, 12, 15, 12, 9, 6],
			[6, 9, 12, 15, 12, 9, 6],
		]

		score = 0
		for row in range(ROW_COUNT):
			for col in range(COLUMN_COUNT):
				if(board[row][col] == player.position):
					score += (weights[row][col])
				elif(board[row][col] == player.opponent.position):
					score -= (weights[row][col])
		
		return score


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
		env.history[player.position - 1].append(column_move)
		return env

	def min_val(self, env, player, target_depth, curr_depth, alpha, beta):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return 6900 * (target_depth - curr_depth + 1)
		
		if(target_depth == curr_depth):
			return -1 * self.evaluation_func(env.board, player)

		v = math.inf
		possible = env.topPosition >= 0
		indices = []

		
		for i, p in enumerate(possible):
			if p: 
				indices.append(i)

		random.shuffle(indices)
		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.max_val(simulated_move, player.opponent, target_depth, curr_depth + 1, alpha, beta)
			if(result < v):
				v = result

			if(v <= alpha):
				return v
			
			beta = min(beta, v)
		
		return v

	def max_val(self, env, player, target_depth, curr_depth, alpha, beta):
		opponent_position = player.opponent.position - 1
		if(len(env.history[opponent_position]) > 0 and env.gameOver(env.history[opponent_position][len(env.history[opponent_position]) - 1], player.opponent.position)):
			return -6900 * (target_depth - curr_depth + 1)

		if(target_depth == curr_depth):
			return self.evaluation_func(env.board, player)

		v = -math.inf
		possible = env.topPosition >= 0
		indices = []

		for i, p in enumerate(possible):
			if p: 
				indices.append(i)

		random.shuffle(indices)
		for play in indices:
			simulated_move = self.simulateMove(env.getEnv(), play, player)
			result = self.min_val(simulated_move, player.opponent, target_depth, curr_depth + 1, alpha, beta)
			if(result > v):
				v = result

			if(v >= beta):
				return v
			
			alpha = max(alpha, v)
		
		return v

	def evaluation_func(self, board, player):
		weights = [
			[3, 6, 9, 12, 9, 6, 3],
			[6, 9, 12, 15, 12, 9, 6],
			[9, 12, 15, 18, 15, 12, 9],
			[9, 12, 15, 18, 15, 12, 9],
			[6, 9, 12, 15, 12, 9, 6],
			[6, 9, 12, 15, 12, 9, 6],
		]

		score = 0
		for row in range(ROW_COUNT):
			for col in range(COLUMN_COUNT):
				if(board[row][col] == player.position):
					score += (weights[row][col])
				elif(board[row][col] == player.opponent.position):
					score -= (weights[row][col])
		
		return score
 
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




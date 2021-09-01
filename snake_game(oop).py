import pygame
import random
import json
pygame.init()
win = pygame.display.set_mode((400, 500))


class Snake:
	""" The Snake Class or the player's character """
	def __init__(self):
		# horizontal speed of snake
		self.vel_x = 10
		# vertical speed of snake
		self.vel_y = 0
		self.head_x = ""
		self.head_y = ""
		# The snake body list will contain the properties of each segment or part of the snake's body in form of lists
		# And in each list, the first item is the x-axis while the second item is the x-axis, the remaining items.. 
		# ..are the respective velocities. The snake's head is the first and only list item in the snake body's list for now
		self.body = [[20, 20, self.vel_x, self.vel_y]]	
		self.width = 10
		self.movinghorizontally = True
		self.movingvertically = False
		# This stores the points at which the snake turns and the new velocity after the turn
		self.body_turns = []

	def draw_body(self):
		for body in self.body:
			pygame.draw.rect(win, (0, 255, 0), (body[0], body[1], self.width, self.width))

	def move_body(self):
		if not game_lost:
			self.body[0][2] = self.vel_x
			self.body[0][3] = self.vel_y

			# All the bodies in the snake's body will each move by their own personal velocities
			for body in self.body:
				body[0] += body[2]
				body[1] += body[3]
			if len(self.body) > 1:
				# If any of the snake's body segments reaches any of the turning points, their velocities are to be replaced..  
				# ..with the ones stored at that point and this would make the snake's body turn
				for body in self.body[1:]:
					for turn in self.body_turns:
						if body[0] == turn[0] and body[1] == turn[1]:
							body[2] = turn[2]
							body[3] = turn[3]
							if body == self.body[-1]:
								self.body_turns.remove(turn)

			self.head_x = self.body[0][0]
			self.head_y = self.body[0][1]

	def out_of_screen_movement(self):
		"""Controls the snake's movement when it goes off screen"""
		for body in self.body:
			if body[1] < 20:
				body[1] = 500
			if body[1] > 500:
				body[1] = 20
			if body[0] > 400:
				body[0] = 0
			if body[0] < 0:
				body[0] = 400

	def check_movement_direction(self):
		"""controls the movement of the snake"""
		if self.vel_x != 0:
			self.movinghorizontally = True
			self.movingvertically = False
		if self.vel_y != 0:
			self.movingvertically = True
			self.movinghorizontally = False

	def save_turning_point(self):
		if len(self.body) > 1:
			self.body_turns.append([self.head_x, self.head_y, self.vel_x, self.vel_y])

	def check_for_collision_with_body(self):
		"""Checks if the head of the snake colides with any other part of the snake"""
		global game_lost
		for body in self.body[1:]:
			if self.vel_x != 0 and body[2] == 0:
				if self.head_y == body[1]:
					if self.head_x == body[0] + self.width:
						game_lost = True
					elif self.head_x + self.width == body[0]:
						game_lost = True
					elif self.head_x == body[0] and self.head_y == body[1]:
						game_lost = True

			if self.vel_y != 0 and body[3] == 0:
				if self.head_x == body[0]:
					if self.head_y == body[1] + self.width:
						game_lost = True
					elif self.head_y + self.width == body[1]:
						game_lost = True
					elif self.head_x == body[0] and self.head_y == body[1]:
						game_lost = True

	def grow_body(self):
		"""Creates a new body at the end of the moving snake by using the velocities of tthe last item or body
			Example: If the last body of the snake is moving left, then we know that it has a 
			negative horizontal speed(-self.body[-1][2]) and zero vertical speed and since each body is 10px wide,
			we can use the equation below to get the new body's coordinate 
		"""
		new_body = [self.body[-1][0] - (self.body[-1][2]), self.body[-1][1] - (self.body[-1][3]), self.body[-1][2], self.body[-1][3]]
		self.body.append(new_body)

snake = Snake()


class Snake_food:
	"""The food class"""
	def __init__(self):
		self.width = 10
		self.x_pos = random.randrange(0, 400, 10)
		self.y_pos = random.randrange(20, 500, 10)
		self.eaten = False
		self.colour  = (255, 0, 0)

	def draw(self):
		pygame.draw.rect(win, self.colour, (self.x_pos, self.y_pos, self.width, self.width))

	def spawn(self):
		for body in snake.body:
			if self.eaten:
				self.x_pos = random.randrange(0, 400, 10)
				self.y_pos = random.randrange(20, 500, 10)
				# This is to prevent the food from spawning on the snake's body 
				if self.x_pos != body[0] and self.y_pos != body[1]:
					self.eaten =  False
				else:
					self.spawn()


run =  True
game_lost = False
text = pygame.font.SysFont("Helvetica", 18)
score = 0
highscore = ""
new_highscore = False
food  = Snake_food()

def load_high_score():
	global highscore
	with open("highscore.json") as highscore_file:
		highscore = json.load(highscore_file)
	if new_highscore:
		with open("highscore.json", "w") as highscore_file:
			json.dump(score, highscore_file)

def restart_game():
	"""Restores important data to their initial values"""
	global game_lost, new_highscore, score
	score = 0
	snake.vel_x = 10
	snake.vel_y = 0
	snake.body_turns = []
	snake.body = [[20, 20, snake.vel_x, snake.vel_y]]
	game_lost = False
	new_highscore = False

def display_game_over_msg():
	pygame.draw.rect(win, (255, 255, 255), (100, 50, 230, 150))
	pygame.draw.rect(win, (0, 0, 255), (100, 50, 230, 30))
	win.blit(text.render("GAME OVER!", False, (255, 0, 0)), (150, 55))
	win.blit(text.render("Press SPACE to play again", True, (0, 255, 0)), (130, 100))
	if new_highscore:
		win.blit(text.render("NEW HIGH SCORE: " + str(score), True, (255, 0, 0)), (130, 155))

while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if not snake.movinghorizontally:
				if event.key == pygame.K_LEFT:
					snake.movinghorizontally = True
					snake.vel_x = -10
					snake.vel_y = 0
					snake.save_turning_point()
				if event.key == pygame.K_RIGHT:
					snake.movinghorizontally = True
					snake.vel_x = 10
					snake.vel_y  = 0
					snake.save_turning_point()
			if not snake.movingvertically:
				if event.key == pygame.K_UP:
					snake.movingvertically = True
					snake.vel_x = 0
					snake.vel_y  = -10
					snake.save_turning_point()
				if event.key == pygame.K_DOWN:
					snake.movingvertically = True
					snake.vel_x = 0
					snake.vel_y  = 10
					snake.save_turning_point()
			if game_lost:
				if event.key == pygame.K_SPACE:
					restart_game()

	load_high_score()
	win.fill((0, 150, 0))
	pygame.draw.rect(win, (100, 100, 100), (0, 0, 400, 20))
	win.blit(text.render("SCORE: " + str(score), True, (0, 255, 0)), (320, 0))
	win.blit(text.render("HIGH SCORE: " + str(highscore), True, (0, 255, 0)), (5, 0))
	snake.draw_body()
	snake.move_body()
	snake.out_of_screen_movement()
	snake.check_movement_direction()
	snake.check_for_collision_with_body()
	food.draw()
	food.spawn()

	if snake.head_y == food.y_pos and snake.head_x == food.x_pos:
		food.eaten = True
		snake.grow_body()
		score += 1

	if game_lost:
		display_game_over_msg()
		if score > highscore:
			new_highscore = True
		
	pygame.display.update()
pygame.quit()
import pygame
import random
run =  True
win = pygame.display.set_mode((400, 500))

class Snake:
	def __init__(self):
		self.vel_x = 10
		self.vel_y = 0
		self.head_x = ""
		self.head_y = ""
		self.body = [[20, 20, self.vel_x, self.vel_y]]	
		self.width = 10
		self.movinghorizontally = True
		self.movingvertically = False
		self.body_turns = []

	def draw_body(self):
		for body in self.body:
			pygame.draw.rect(win, (0, 255, 0), (body[0], body[1], self.width, self.width))
			
	def move_body(self):
		self.body[0][2] = self.vel_x
		self.body[0][3] = self.vel_y

		for body in self.body:
			body[0] += body[2]
			body[1] += body[3]
		if len(self.body) > 1:
			for body in self.body[1:]:
				for turn in self.body_turns:
					if body[0] == turn[0] and body[1] == turn[1]:
						body[2] = turn[2]
						body[3] = turn[3]
						if body == self.body[-1]:
							self.body_turns.remove(turn)

		self.head_x = self.body[0][0]
		self.head_y = self.body[0][1]

	def check_movement_direction(self):
		if self.vel_x != 0:
			self.movinghorizontally = True
			self.movingvertically = False
		if self.vel_y != 0:
			self.movingvertically = True
			self.movinghorizontally = False

	def grow_body(self):
		new_body = [self.body[-1][0] - (self.body[-1][2]), self.body[-1][1] - (self.body[-1][3]), self.body[-1][2], self.body[-1][3]]
		self.body.append(new_body)


class Snake_food:
	def __init__(self):
		self.width = 10
		self.x_pos = random.randrange(0, 400, 10)
		self.y_pos = random.randrange(0, 500, 10)
		self.eaten = False
		self.colour  = (255, 0, 0)

	def draw(self):
		pygame.draw.rect(win, self.colour, (self.x_pos, self.y_pos, self.width, self.width))

	def spawn(self):
		if self.eaten:
			self.x_pos = random.randrange(0, 400, 10)
			self.y_pos = random.randrange(0, 500, 10)
			self.eaten =  False


snake = Snake()
food  = Snake_food()

while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if not snake.movinghorizontally:
				if event.key == pygame.K_LEFT:
					snake.vel_x = -10
					snake.vel_y = 0
					if len(snake.body) > 1:
						snake.body_turns.append([snake.head_x, snake.head_y, snake.vel_x, snake.vel_y])
					snake.movinghorizontally = True
				if event.key == pygame.K_RIGHT:
					snake.vel_x = 10
					snake.vel_y  = 0
					if len(snake.body) > 1:
						snake.body_turns.append([snake.head_x, snake.head_y, snake.vel_x, snake.vel_y])
					snake.movinghorizontally = True
			if not snake.movingvertically:
				if event.key == pygame.K_UP:
					snake.vel_x = 0
					snake.vel_y  = -10
					if len(snake.body) > 1:
						snake.body_turns.append([snake.head_x, snake.head_y, snake.vel_x, snake.vel_y])
					snake.movingvertically = True
				if event.key == pygame.K_DOWN:
					snake.vel_x = 0
					snake.vel_y  = 10
					if len(snake.body) > 1:
						snake.body_turns.append([snake.head_x, snake.head_y, snake.vel_x, snake.vel_y])
					snake.movingvertically = True

	win.fill((0, 0, 0))
	snake.draw_body()
	snake.move_body()
	snake.check_movement_direction()
	food.draw()
	food.spawn()
	if snake.head_y == food.y_pos and snake.head_x == food.x_pos:
		food.eaten = True
		snake.grow_body()
	# print(snake.body_turns)

	pygame.display.update()
pygame.quit()
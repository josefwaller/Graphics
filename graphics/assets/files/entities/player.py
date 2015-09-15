from .jumping_entity import JumpingEntity
from ..utilities.globals import Globals

import time
import pygame

class Player (JumpingEntity):

	x_translate = 0
	speed = 300

	jump_strength = 13
	momY = 0
	is_grounded = True

	last_time = 0
	delta_time = 0

	last_move_time = 0

	is_dead = None

	def __init__(self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = int(10 * (Globals.block_size / 16))
		self.h = int(19 * (Globals.block_size / 16))

		self.is_dead = False

		self.jump_strength *= Globals.block_size

		self.sprites = [
			pygame.image.load("assets/images/player/run_1.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_2.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_3.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_2.png").convert_alpha(),
		]

		self.sprite_indexes = [
			1
		]

		self.jump_last_time = time.time()

		self.is_animated = True
		self.sprite_interval = 100

		self.last_move_time = time.time()

	def while_keys_down (self, keys):

		if pygame.K_LEFT in keys:

			self.x_translate = -1
			self.sprite_indexes = range(4)
			self.facing_left = True

		if pygame.K_RIGHT in keys:

			self.x_translate = 1
			self.sprite_indexes = range(4)
			self.facing_left = False

		if pygame.K_RIGHT not in keys and pygame.K_LEFT not in keys:

			self.x_translate = 0
			self.sprite_indexes = [1]

		if pygame.K_UP in keys and self.is_grounded:

			self.start_jump()


	def move (self):

		self.x += self.x_translate * self.speed * self.delta_time

		for enemy in Globals.enemies:

			if enemy.x < self.x + self.w:
				if enemy.x + enemy.w > self.x:

					if enemy.y > self.y + self.h:
						if enemy.y + enemy.h < self.y:

							self.id_dead = True
							print("is dead")


	def update (self):

		self.set_delta_time()

		self.move()

		if self.x >= Globals.window.get_size()[0] / 2:

			Globals.camera_offset['x'] = - (self.x - Globals.window.get_size()[0] / 2)

		self.gravity_update()

		self.render()
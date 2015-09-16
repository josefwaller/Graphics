from assets.files.utilities.globals import Globals
from assets.files.entities.enemies.base_enemy import BaseEnemy

import time
import pygame

class Archer (BaseEnemy):

	last_arrow_time = None
	arrow_delay = None

	is_attacking = None
	attack_duration = None

	def __init__ (self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.w = int((Globals.block_size/16) * 11)
		self.h = int((Globals.block_size/16) * 13)

		self.last_arrow_time = time.time()

		self.sprites = [

			pygame.image.load("assets/images/enemies/archer/archer_1.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/archer/archer_2.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/archer/archer_shoot.png").convert_alpha()

		]

		self.is_animated = True

		self.idle_indexes = [0, 1]
		self.attack_indexes = [2]

		self.sprite_indexes = self.idle_indexes
		self.sprite_interval = 300

		self.last_arrow_time = time.time()
		self.arrow_delay = 2
		self.is_attacking = False
		self.attack_duration = 0.1

	def attack (self):

		if self.is_attacking:

			if time.time() - self.attack_time >= self.attack_duration:

				self.is_attacking = False
				self.facing_left = False
				self.sprite_indexes = self.idle_indexes

				self.last_arrow_time = time.time()

		else:

			if Globals.player.x > self.x:
				self.facing_left = True

			else:
				self.facing_left = False

			if time.time() - self.last_arrow_time >= self.arrow_delay:

				self.sprite_indexes = self.attack_indexes

				if self.facing_left:
					direction = 1
				else:
					direction = -1

				Globals.enemies.append(Arrow(x=self.x, y=self.y + int(self.h / 2), direction=direction))

				self.attack_time = time.time()
				self.is_attacking = True


	def update (self):

		self.set_delta_time()

		self.attack()

		self.gravity_update()

		self.check_for_player_collision()

		self.render()



class Arrow (BaseEnemy):

	def __init__ (self, x, y, direction):

		self.x = x
		self.y = y

		self.speed = 5 * Globals.block_size

		self.w = self.make_pixelated(6)
		self.h = self.make_pixelated(3)

		self.image = pygame.image.load("assets/images/enemies/archer/arrow.png").convert_alpha()

		self.direction = direction

		if self.direction == 1:
			self.facing_left = True

		else:
			self.facing_left = False

	def move (self):

		self.x += self.speed * self.delta_time * self.direction

		if self.is_grounded:

			Globals.enemies.remove(self)
			return

	def update (self):

		self.set_delta_time()

		self.move()

		self.gravity_update()

		self.check_for_player_collision()

		self.render()
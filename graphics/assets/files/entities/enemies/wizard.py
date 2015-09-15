from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import time
import pygame

class Wizard (BaseEntity):

	last_missile_time = None
	missile_delay = None
	missiles = None

	is_attacking = None
	attack_time = None
	attack_duration = None

	def __init__(self, x, y, time_offset=0, missile_delay=1):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.last_missile_time = time.time() + (time_offset * 1000)
		self.missile_delay = missile_delay
		self.missiles = []

		self.sprites = [
			pygame.image.load("assets/images/enemies/wizard/front.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/wizard/side.png").convert_alpha()
		]

		self.is_animated = True

		self.sprite_indexes = [0]

		self.attack_duration = 1

		self.w = Globals.block_size
		self.h = Globals.block_size

	def update (self):

		if self.is_attacking:

			if time.time() - self.attack_time >= self.attack_duration:

				self.is_attacking = False
				self.facing_left = False
				self.sprite_indexes = [0]

				self.last_missile_time = time.time()

		else:

			if time.time() - self.last_missile_time >= self.missile_delay:
				Globals.enemies.append(Missile(x=self.x, y=self.y, starting_time=time.time()))

				self.sprite_indexes = [1]

				if Globals.player.x > self.x:
					self.facing_left = True

				else:
					self.facing_left = False

				self.attack_time = time.time()
				self.is_attacking = True

		self.render()


class Missile (BaseEntity):

	lifespan = None
	starting_time = None
	speed = None

	def __init__(self, x, y, starting_time):

		self.x = x
		self.y = y

		self.w = Globals.block_size
		self.h = Globals.block_size
		self.lifespan = 3

		self.speed = 200

		self.starting_time = starting_time

		self.is_animated = False
		self.image = pygame.image.load("assets/images/blocks/temp_block.png").convert_alpha()

	def move (self):

		x_translate = 0
		y_translate = 0

		if Globals.player.x  > self.x:

			x_translate = 1

		elif Globals.player.x < self.x + self.w:

			x_translate = -1

		if Globals.player.y > self.y + self.h:

			y_translate = 1

		elif Globals.player.y < self.y - self.h:

			y_translate = -1

		self.x += self.speed * x_translate * self.delta_time
		self.y += self.speed * y_translate * self.delta_time

		if time.time() - self.starting_time >= self.lifespan:
			Globals.enemies.remove(self)


	def update(self):

		self.set_delta_time()

		self.move()

		self.render()

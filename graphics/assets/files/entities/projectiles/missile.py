from assets.files.utilities.globals import Globals

from assets.files.entities.base_entity import BaseEntity

import pygame
import time


class Missile (BaseEntity):

	lifespan = None
	starting_time = None
	speed = None

	momX = None
	moxY = None

	def __init__(self, x, y, direction=1, is_enemy=True):

		self.x = x
		self.y = y

		self.w = int(3 * (Globals.block_size/16))
		self.h = int(3 * (Globals.block_size/16))
		self.lifespan = 1

		self.speed = 5

		self.is_enemy = is_enemy

		self.starting_time = time.time()

		self.momX = 30 * direction
		self.momY = 0

		self.turn_speed = 5

		self.is_animated = False
		self.image = pygame.image.load("assets/images/enemies/wizard/missile.png").convert_alpha()

	def move (self):

		x_translate = 0
		y_translate = 0

		if self.is_enemy:

			if Globals.player.x  + Globals.player.w > self.x:

				x_translate = 1

			elif Globals.player.x < self.x + self.w:

				x_translate = -1

			if Globals.player.y > self.y:

				y_translate = 1

			elif Globals.player.y + Globals.player.h < self.y:

				y_translate = -1

			self.momX += x_translate * self.turn_speed
			self.momY += y_translate * self.turn_speed

			self.x += self.momX * self.speed * self.delta_time
			self.y += self.momY * self.speed * self.delta_time

			if self.is_enemy:

				if self.check_for_collision(Globals.player):
					Globals.player.on_hit()

			if time.time() - self.starting_time >= self.lifespan:
				Globals.projectiles.remove(self)


	def update(self):

		self.set_delta_time()

		self.move()

		self.render()

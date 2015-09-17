from assets.files.utilities.globals import Globals
from assets.files.entities.base_entity import BaseEntity

import pygame
class Checkpoint (BaseEntity):

	flag = None

	flag_risen = False
	flag_rising = False

	flag_speed = None

	def __init__(self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.h = 2 * Globals.block_size

		self.flag = BaseEntity()

		self.flag.w = self.make_pixelated(9)
		self.flag.h = self.make_pixelated(6)

		self.flag.x = self.x
		self.flag.y = self.y + Globals.block_size - self.flag.h
		self.flag.is_animated = False
		self.flag.image = pygame.image.load("assets/images/props/flag.png")

		self.flag_speed = 300

		self.pole = BaseEntity()

		self.pole.x = self.x
		self.pole.y = self.y - int(self.h / 2)

		self.pole.w = self.make_pixelated(2)
		self.pole.h = self.h
		self.pole.is_animated = False
		self.pole.image = pygame.image.load("assets/images/props/pole.png")

	def update (self):

		self.set_delta_time()

		if self.check_for_collision(Globals.player):
			Globals.player.checkpoint = self
			self.flag_rising = True

		if self.flag_rising:
			self.flag.y -= self.flag_speed * self.delta_time

			if self.flag.y <= self.pole.y:
				self.flag_rising = False
				self.flag_risen = True
				self.flag.y = self.pole.y

		self.render()

	def render (self):

		self.flag.render()
		self.pole.render()


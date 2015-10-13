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
		self.y -= self.h

		self.flag = BaseEntity()

		self.flag.w = self.make_pixelated(9)
		self.flag.h = self.make_pixelated(6)

		self.flag.x = self.x
		self.flag.y = self.y + self.h - self.flag.h
		self.flag.is_animated = False
		self.flag.graphic_images = [
			self.img_load("props/flag.png"),
			self.img_load("props/16_flag.png")
		]
		self.flag.image = self.flag.graphic_images[0]
		self.flag.facing_left = True

		self.flag_speed = 300

		self.pole = BaseEntity()

		self.pole.x = self.flag.x + self.flag.w
		self.pole.y = self.y

		self.pole.w = self.make_pixelated(2)
		self.pole.h = self.h
		self.pole.is_animated = False
		self.pole.graphic_images = [
			self.img_load("props/pole.png"),
			self.img_load("props/16_pole.png")
		]
		self.pole.image = self.pole.graphic_images[0]

		self.hitboxes = []

		self.add_hitbox(x=0, y=0, w=self.pole.w, h=32)

	def update_graphics (self):

		self.flag.update_graphics()
		self.pole.update_graphics()

	def update (self):


		if self.check_for_collision(Globals.player):
			Globals.player.checkpoint = self
			self.flag_rising = True

		if self.flag_rising:
			self.flag.y -= self.flag_speed * self.delta_time

			if self.flag.y <= self.pole.y:
				self.flag_rising = False
				self.flag_risen = True
				self.flag.y = self.pole.y
				print("flag risen")

		self.render()

	def render (self):

		self.flag.render()
		self.pole.render()



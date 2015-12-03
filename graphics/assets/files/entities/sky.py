from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import pygame


class Sky (BaseEntity):

	x_addon = 0
	sky_image = None

	def __init__(self):
		self.x = Globals.camera_offset['x'] / 20
		self.w = Globals.window.get_size()[0]
		self.h = Globals.window.get_size()[1]

		self.is_animated = False

		self.graphic_images = [
			self.img_load("props/t_sky.png"),
			self.img_load("props/8_sky.png"),
			self.img_load("props/16_sky.png")
		]

		self.image = self.graphic_images[Globals.graphics_level]

		self.is_static = True

		converter = self.image.get_size()[0] / self.image.get_size()[1]
		self.w = int(self.w * converter)

		self.hitboxes = []

	def update(self):

		self.x = Globals.camera_offset['x'] / 20

	def render(self):

		img = pygame.transform.scale(self.image, (self.w, self.h))

		Globals.window.blit(img, (self.x, 0))

from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import pygame

class Sky (BaseEntity):

	x_addon = 0
	sky_image = None

	def __init__ (self):
		self.x_addon = 0
		self.w = Globals.window.get_size()[0]
		self.h = Globals.window.get_size()[1]

		img = self.img_load("props/sky.png")
		converter = img.get_size()[0] / img.get_size()[1]
		self.sky_image = pygame.transform.scale(img, (int(converter * self.w), self.h))

	def update (self):

		Globals.window.blit(self.sky_image, (0 + Globals.camera_offset['x'] / 20, 0))

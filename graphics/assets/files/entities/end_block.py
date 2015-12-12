from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import time
import pygame


class EndBlock (BaseEntity):

	def __init__(self, x, y):

		if Globals.graphics_level == 0:
			self.graphic_images = [
				self.img_load("blocks/t_up_graphics_8.png"),
				self.img_load("blocks/8_up_graphics_8.png")
			]
		elif Globals.graphics_level == 1:
			self.graphic_images = [
				self.img_load("blocks/8_up_graphics_16.png"),
				self.img_load("blocks/16_up_graphics_16.png")
			]
		else:
			pass

		self.image = self.graphic_images[0]

		self.is_animated = False
		self.is_static = True

		self.w, self.h = 16, 16

		self.facing_left = True

		self.add_hitbox(0, 0, 16, 16)
		self.used = False

		self.entity_init(x, y)

		self.update_graphics()

	def update(self):

		if self.check_for_collision(Globals.player) and not self.used:

			# Globals.is_paused = True
			#
			# Globals.hud.message_box(
			# 	title="Congratulations!",
			# 	message=
			# 	"Congratulations! You have now unlocked 16-Bit graphics! Enjoy the beautiful look of high end graphics! "
			# 	"\n \n Press ENTER to continue...",
			# 	fade_out=True)

			self.used = True

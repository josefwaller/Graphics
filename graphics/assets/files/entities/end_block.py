from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import json


class EndBlock (BaseEntity):

	def __init__(self, x, y):

		self.graphic_images = [
			self.img_load("blocks/8_up_graphics_8.png"),
			self.img_load("blocks/16_up_graphics_16.png"),
			self.img_load("blocks/3d_end_block.png")
		]

		self.image = self.graphic_images[Globals.graphics_level]

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

			if Globals.graphics_level == 2:
				Globals.hud.show_credits()
				self.used = True
				return

			Globals.is_paused = True

			file = open("assets/dialog/eb_%s.json" % (Globals.graphics_level + 1), "r")
			file_contents = json.loads(file.read())
			file.close()

			Globals.hud.message_box(
				title=file_contents['title'],
				message=file_contents['message'],
				fade_out=True)

			self.used = True

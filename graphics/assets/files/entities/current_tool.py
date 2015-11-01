from assets.files.entities.base_entity import BaseEntity

from assets.files.utilities.globals import Globals

class CurrentTool (BaseEntity):

	def __init__ (self):

		self.graphic_sprites = [
			[
				self.img_load("player/sword_1.png"),
				self.img_load("player/sword_2.png"),
				self.img_load("player/sword_3.png"),

				self.img_load("player/bar_1.png"),
				self.img_load("player/bar_2.png"),
				self.img_load("player/bar_3.png"),

				self.img_load("player/sword_swing_1.png"),
				self.img_load("player/sword_swing_2.png"),
				self.img_load("player/sword_swing_3.png"),
				self.img_load("player/sword_swing_4.png"),

				self.img_load("player/bar_shoot_1.png"),
				self.img_load("player/bar_shoot_2.png"),
				self.img_load("player/bar_shoot_3.png"),
			],
			[
				self.img_load("player/16_sword_1.png"),
				self.img_load("player/16_sword_2.png"),
				self.img_load("player/16_sword_3.png"),

				self.img_load("player/16_bar_1.png"),
				self.img_load("player/16_bar_2.png"),
				self.img_load("player/16_bar_3.png")
			]
		]

		self.sprites = self.graphic_sprites[0]

		self.x = Globals.player.x
		self.y = Globals.player.y

		self.img_w = Globals.player.img_w
		self.img_h = Globals.player.img_h

		self.least_x = 0

		self.is_animated = True

		self.sprite_indexes = [0]

		self.is_showing = True

		self.resize_images()
		self.is_static = True

	def update (self):

		self.x = Globals.player.x - Globals.player.least_x
		self.y = Globals.player.y - Globals.player.least_y

		self.facing_left = Globals.player.facing_left

		if self.is_showing:

			self.render()
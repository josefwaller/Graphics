from assets.files.entities.base_entity import BaseEntity

from assets.files.utilities.globals import Globals

class CurrentTool (BaseEntity):

	def __init__ (self):

		self.graphic_sprites = [
			[
				self.img_load("player/temp/t_sword_1.png"),
				self.img_load("player/temp/t_sword_2.png"),
				self.img_load("player/temp/t_sword_3.png"),

				self.img_load("player/temp/t_sword_swing_1.png"),
				self.img_load("player/temp/t_sword_swing_2.png"),
				self.img_load("player/temp/t_sword_swing_3.png"),
				self.img_load("player/temp/t_sword_swing_4.png"),

				self.img_load("player/temp/t_sword_jump.png"),
				self.img_load("player/temp/t_sword_fall.png"),

				self.img_load("player/temp/t_bar_1.png"),
				self.img_load("player/temp/t_bar_2.png"),
				self.img_load("player/temp/t_bar_3.png"),

				self.img_load("player/temp/t_bar_shoot_1.png"),
				self.img_load("player/temp/t_bar_shoot_2.png"),
				self.img_load("player/temp/t_bar_shoot_3.png"),

				self.img_load("player/8bit/8_bar_jump.png"),
				self.img_load("player/8bit/8_bar_fall.png"),

				self.img_load("player/8bit/8_staff_1.png"),
				self.img_load("player/8bit/8_staff_2.png"),
				self.img_load("player/8bit/8_staff_3.png"),

				self.img_load("player/8bit/8_staff_swing_1.png"),
				self.img_load("player/8bit/8_staff_swing_2.png"),
				self.img_load("player/8bit/8_staff_swing_3.png"),
				self.img_load("player/8bit/8_staff_swing_4.png"),

				self.img_load("player/8bit/8_staff_jump.png"),
				self.img_load("player/8bit/8_staff_fall.png"),
			],
			[
				self.img_load("player/8bit/8_sword_1.png"),
				self.img_load("player/8bit/8_sword_2.png"),
				self.img_load("player/8bit/8_sword_3.png"),

				self.img_load("player/8bit/8_sword_swing_1.png"),
				self.img_load("player/8bit/8_sword_swing_2.png"),
				self.img_load("player/8bit/8_sword_swing_3.png"),
				self.img_load("player/8bit/8_sword_swing_4.png"),

				self.img_load("player/8bit/8_sword_jump.png"),
				self.img_load("player/8bit/8_sword_fall.png"),

				self.img_load("player/8bit/8_bar_1.png"),
				self.img_load("player/8bit/8_bar_2.png"),
				self.img_load("player/8bit/8_bar_3.png"),

				self.img_load("player/8bit/8_bar_shoot_1.png"),
				self.img_load("player/8bit/8_bar_shoot_2.png"),
				self.img_load("player/8bit/8_bar_shoot_3.png"),

				self.img_load("player/8bit/8_bar_jump.png"),
				self.img_load("player/8bit/8_bar_fall.png"),

				self.img_load("player/8bit/8_staff_1.png"),
				self.img_load("player/8bit/8_staff_2.png"),
				self.img_load("player/8bit/8_staff_3.png"),

				self.img_load("player/8bit/8_staff_swing_1.png"),
				self.img_load("player/8bit/8_staff_swing_2.png"),
				self.img_load("player/8bit/8_staff_swing_3.png"),
				self.img_load("player/8bit/8_staff_swing_4.png"),

				self.img_load("player/8bit/8_staff_jump.png"),
				self.img_load("player/8bit/8_staff_fall.png"),
			],
			[
				self.img_load("player/16bit/16_sword_1.png"),
				self.img_load("player/16bit/16_sword_2.png"),
				self.img_load("player/16bit/16_sword_3.png"),

				self.img_load("player/16bit/16_sword_swing_1.png"),
				self.img_load("player/16bit/16_sword_swing_2.png"),
				self.img_load("player/16bit/16_sword_swing_3.png"),
				self.img_load("player/16bit/16_sword_swing_4.png"),

				self.img_load("player/16bit/16_sword_jump.png"),
				self.img_load("player/16bit/16_sword_fall.png"),

				self.img_load("player/16bit/16_bar_1.png"),
				self.img_load("player/16bit/16_bar_2.png"),
				self.img_load("player/16bit/16_bar_3.png"),

				self.img_load("player/16bit/16_bar_shoot_1.png"),
				self.img_load("player/16bit/16_bar_shoot_2.png"),
				self.img_load("player/16bit/16_bar_shoot_3.png"),

				self.img_load("player/16bit/16_bar_jump.png"),
				self.img_load("player/16bit/16_bar_fall.png"),

				self.img_load("player/16bit/16_staff_1.png"),
				self.img_load("player/16bit/16_staff_2.png"),
				self.img_load("player/16bit/16_staff_3.png"),

				self.img_load("player/16bit/16_staff_swing_1.png"),
				self.img_load("player/16bit/16_staff_swing_2.png"),
				self.img_load("player/16bit/16_staff_swing_3.png"),
				self.img_load("player/16bit/16_staff_swing_4.png"),

				self.img_load("player/16bit/16_staff_jump.png"),
				self.img_load("player/16bit/16_staff_fall.png"),
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

		if not self.last_graphics == Globals.player.last_graphics:
			self.update_graphics()

		self.x = Globals.player.x - Globals.player.least_x
		self.y = Globals.player.y - Globals.player.least_y

		self.facing_left = Globals.player.facing_left

		self.animate()

		if self.is_showing:

			self.render()

	def animate (self):

		p = Globals.player

		if p.tool == None:
			self.is_showing = False

		else:

			self.is_showing = True

		if self.is_showing:
			if not p.is_showing: 
				self.is_showing = False
				return

			try:

				i = p.sprite_indexes[p.this_index]

			except IndexError:
				print("Tool Sprite IndexOutOfRange!")
				print("p.this_index: %s" % p.this_index)
				#The player will call an error for this

			if not p.using_tool:
				s = i

				if i == 10 or i == 11:
					if p.tool == "Bow and Arrow":
						s = i - 4
					else:
						s = i - 3

				if p.tool == "Bow and Arrow":

					self.sprite_indexes = [s + 9]

				elif p.tool == "Sword":
					self.sprite_indexes = [s]

				elif p.tool == "Staff":
					self.sprite_indexes = [s + 17]

			elif p.using_tool:

				if p.tool == "Bow and Arrow":

					self.sprite_indexes = [i + 9]

				elif p.tool == "Sword":

					self.sprite_indexes = [i - 3]

				elif p.tool == "Staff":

					self.sprite_indexes = [i + 14]
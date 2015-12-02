from assets.files.entities.base_entity import BaseEntity

from assets.files.utilities.globals import Globals


class CurrentTool (BaseEntity):

	def __init__(self):

		# Sets the graphic sprites

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

				self.img_load("player/temp/t_bar_jump.png"),
				self.img_load("player/temp/t_bar_fall.png"),

				self.img_load("player/temp/t_staff_1.png"),
				self.img_load("player/temp/t_staff_2.png"),
				self.img_load("player/temp/t_staff_3.png"),

				self.img_load("player/temp/t_staff_swing_1.png"),
				self.img_load("player/temp/t_staff_swing_2.png"),
				self.img_load("player/temp/t_staff_swing_3.png"),
				self.img_load("player/temp/t_staff_swing_4.png"),

				self.img_load("player/temp/t_staff_jump.png"),
				self.img_load("player/temp/t_staff_fall.png"),
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

		# Copies the player's position
		self.x = Globals.player.x
		self.y = Globals.player.y

		# Copies the player's image dimensions
		self.w = Globals.player.sprites[0].get_size()[0]
		self.h = Globals.player.sprites[0].get_size()[1]

		self.image_offset_x = 0

		# Sets misc variables
		self.is_animated = True
		self.sprite_indexes = [0]
		self.is_showing = True
		self.is_static = True
		self.resize_images()

	# Called every framr

	def update (self):

		# Checks for graphics update
		if not self.last_graphics == Globals.player.last_graphics:
			self.update_graphics()

		# Updates position to match player's
		self.x = Globals.player.x - Globals.player.image_offset_x
		self.y = Globals.player.y - Globals.player.image_offset_y

		self.facing_left = Globals.player.facing_left

		# Animates self
		self.animate()

		# Checks if it should render, and then does
		if self.is_showing:
			self.render()

	# Finds the right index to match the player
	# Finds the right tool, action, etc
	def animate (self):

		# Gets player for easy reference
		p = Globals.player

		# Checks if the player has a tool
		if p.tool == None:
			self.is_showing = False
		else:
			self.is_showing = True

		if self.is_showing:

			# Checks if the player has lost visibility
			# Only used when the player is hit
			if not p.is_showing: 
				self.is_showing = False
				return

			# copies the player's sprite index
			try:
				i = p.sprite_indexes[p.this_index]
			except IndexError:
				return
				#The player will call an error for this

			# Animates for running, jumping
			if not p.using_tool:

				# Copies the players's index to be edited and used
				s = i

				# If the player is jumping or falling
				if i == 10 or i == 11:
					if p.tool == "Bow and Arrow":
						s = i - 4
					else:
						s = i - 3

				# Sets the index according to what tool the player has
				if p.tool == "Bow and Arrow":
					self.sprite_indexes = [s + 9]

				elif p.tool == "Sword":
					self.sprite_indexes = [s]

				elif p.tool == "Staff":
					self.sprite_indexes = [s + 17]

			# If the player is swinging the sword, drawing the bow etc.
			elif p.using_tool:

				# Sets the index according to what tool the player has
				if p.tool == "Bow and Arrow":
					self.sprite_indexes = [i + 9]

				elif p.tool == "Sword":
					self.sprite_indexes = [i - 3]

				elif p.tool == "Staff":
					self.sprite_indexes = [i + 14]

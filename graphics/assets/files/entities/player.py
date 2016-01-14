from assets.files.entities.jumping_entity import JumpingEntity

from assets.files.entities.projectiles.arrow import Arrow
from assets.files.entities.projectiles.missile import Missile

from assets.files.utilities.globals import Globals

import time
import pygame


class Player (JumpingEntity):

	# Horizontal Direction
	x_translate = 0
	# Speed
	speed = 7
	speedup_duration = 0.1
	speedup_start_time = 0

	jump_strength = 13
	# the sound to play when jumping
	jump_sound = None
	# used to determine jump strength
	jump_time = 0
	max_jump_time = 0.5

	# Vertical Momentum
	momY = 0

	using_tool = False
	arrow_speed = 0

	# The time the toop was used
	tool_time = 0

	# The sword's range
	sword_range = 1

	# The time it takes to recover
	recover_delay = 1.5

	# Variables for blinking after being hit
	is_blinking = False
	last_blink = 0
	blink_delay = 0.1
	blink_start_time = 0


	is_dead = None

	# The most recent checkpoint
	checkpoint = None

	# A string representing the current tool
	tool = None

	def __init__(self, x, y):

		self.is_dead = False

		self.jump_strength *= Globals.block_size
		self.speed *= Globals.block_size
		self.sword_range += Globals.block_size

		self.graphic_sprites = [

			# Temporary
			[
				self.img_load("player/temp/t_run_1.png"),
				self.img_load("player/temp/t_run_2.png"),
				self.img_load("player/temp/t_run_3.png"),

				self.img_load("player/temp/t_shoot_1.png"),
				self.img_load("player/temp/t_shoot_2.png"),
				self.img_load("player/temp/t_shoot_3.png"),

				self.img_load("player/temp/t_swing_1.png"),
				self.img_load("player/temp/t_swing_2.png"),
				self.img_load("player/temp/t_swing_3.png"),
				self.img_load("player/temp/t_swing_4.png"),

				self.img_load("player/temp/t_jump.png"),
				self.img_load("player/temp/t_fall.png")
			],

			# 8-bit
			[
				self.img_load("player/8bit/8_run_1.png"),
				self.img_load("player/8bit/8_run_2.png"),
				self.img_load("player/8bit/8_run_3.png"),

				self.img_load("player/8bit/8_shoot_1.png"),
				self.img_load("player/8bit/8_shoot_2.png"),
				self.img_load("player/8bit/8_shoot_3.png"),

				self.img_load("player/8bit/8_swing_1.png"),
				self.img_load("player/8bit/8_swing_2.png"),
				self.img_load("player/8bit/8_swing_3.png"),
				self.img_load("player/8bit/8_swing_4.png"),

				self.img_load("player/8bit/8_jump.png"),
				self.img_load("player/8bit/8_fall.png")
			],

			# 16-bit
			[
				self.img_load("player/16bit/16_run_1.png"),
				self.img_load("player/16bit/16_run_2.png"),
				self.img_load("player/16bit/16_run_3.png"),

				self.img_load("player/16bit/16_shoot_1.png"),
				self.img_load("player/16bit/16_shoot_2.png"),
				self.img_load("player/16bit/16_shoot_3.png"),

				self.img_load("player/16bit/16_swing_1.png"),
				self.img_load("player/16bit/16_swing_2.png"),
				self.img_load("player/16bit/16_swing_3.png"),
				self.img_load("player/16bit/16_swing_4.png"),

				self.img_load("player/16bit/16_jump.png"),
				self.img_load("player/16bit/16_fall.png")

			]
		]
		# Sets the current sprite set according to the graphics level
		self.sprites = self.graphic_sprites[Globals.graphics_level]

		# Sets the sprite indexes so the player is standing
		self.sprite_indexes = [
			1
		]

		# Loads sounds
		self.jump_sound = self.load_sound("assets/sounds/jump.wav")
		self.arrow_sound = self.load_sound("assets/sounds/arrow.wav")
		self.sword_sound = self.load_sound("assets/sounds/sword.wav")
		self.missile_sound = self.load_sound("assets/sounds/missile.wav")

		# Sets the last time to 0
		# Makes the player start at rest
		self.jump_last_time = time.time()

		self.is_animated = True

		# Sets a 100 millisecond delay between sprite changes
		self.sprite_interval = 100

		# Adds hitboxes
		self.add_hitbox(x=14, y=0, w=11, h=12)
		self.add_hitbox(x=16, y=12, w=6, h=7)

		# Sets width and height in units of 1/16ths of block size
		self.h = 19
		self.w = 38
		
		self.entity_init(x, y)
		self.is_showing = True

	# Called Every frame
	# Interprets Input
	# Parameter keys is keys that are currently down
	def while_keys_down(self, keys):
		if pygame.K_LEFT in keys or pygame.K_RIGHT in keys:

			# Moves left
			if pygame.K_LEFT in keys:
				new_x_translate = -1
				self.facing_left = True

			# Moves Right
			if pygame.K_RIGHT in keys:
				new_x_translate = 1
				self.facing_left = False


			# Checks if it was moving the same way before
			if not self.x_translate == new_x_translate:
				self.speedup_start_time = time.time()

			self.x_translate = new_x_translate

		# Not moving
		else:
			self.speedup_start_time = time.time()
			self.x_translate = 0

		# Checks for jumping
		if pygame.K_UP in keys:

			if not self.using_tool:
				# Starts jump if needed
				if self.is_grounded:
					self.jump_time = time.time()
					self.jump_sound.play(loops=0)
					self.start_jump()

		else:
			if not self.is_grounded:

				# Cancels out three quaters of down momentum
				self.momY -= (Globals.gravity_strength * self.delta_time)

		# Checks for tool use
		if pygame.K_SPACE in keys:

			if self.tool is not None:
				# Sets up tool variables
				if not self.using_tool:
					self.tool_time = time.time()
					if self.tool == "Sword":
						self.sword_sound.play()

				self.using_tool = True

		# For Bow and Arrow, releases arrow
		elif self.using_tool and self.tool == "Bow and Arrow":

			self.use_tool()

		if Globals.debug:

			if pygame.K_k in keys:
				self.respawn()
			elif pygame.K_c in keys:
				Globals.hud.show_credits()
				Globals.playing_credits = True

	# Does misc stuff depending on the tool
	def use_tool(self):

		if self.tool == "Bow and Arrow":

			# Sets the direction
			if self.facing_left:
				direction = -1
			else:
				direction = 1
		
			Globals.projectiles.append(Arrow(
				x=self.x + (self.w / 2),
				y=self.y + int(self.h * (3/5)),
				direction=direction,
				is_enemy=False,
				speed=self.arrow_speed
			))

			self.arrow_sound.play()

			self.using_tool = False

		elif self.tool == "Sword":

			# Swings sword
			for enemy in Globals.enemies:

				# Checks for vertical collision
				if enemy.y + enemy.h > self.y:
					if enemy.y < self.y + self.h:
						for hb in enemy.hitboxes:

							# Checks if it hit anything
							if self.facing_left:
								if hb.x < self.x:
									if hb.x > self.x - self.sword_range:
										enemy.on_hit()

							else:
								if hb.x > self.x + self.w:
									if hb.x < self.x + self.w + self.sword_range:
										enemy.on_hit()

		elif self.tool == "Staff":

			# Finds proper x and direction for missile
			if self.facing_left:
				x = self.x - self.w
				direction = -1

			else:
				x = self.x + self.w + (self.w / 4)
				direction = 1

			# Adds missile
			Globals.projectiles.append(Missile(x=x, y=self.y + self.h * 3/5, is_enemy=False, direction=direction))
			self.missile_sound.play()

	def move(self):

		# Sets idle sprites and running sprites for easy use
		idle_sprites = [1]
		running_sprites = [0, 1, 2, 1]

		# Moves
		if not self.using_tool:
			if not self.x_translate == 0:

				if time.time() - self.speedup_start_time >= self.speedup_duration:
					multiplier = 1
				else:
					multiplier = (time.time() - self.speedup_start_time) / self.speedup_duration
				self.x += multiplier * self.x_translate * self.speed * self.delta_time

			if self.is_grounded:
				# Checks whether the player is standing or running
				if self.x_translate == 0:
					self.sprite_indexes = idle_sprites

				else:
					self.sprite_indexes = running_sprites

			# Checks for falling animation
			else:

				# Checks if the player is falling or jumping
				if self.momY > -150:
					self.sprite_indexes = [10]

				else:
					self.sprite_indexes = [11]

		# Makes sure the player cannot run off the level
		if self.x < 0:
			self.x = 0
		elif self.x > Globals.level_width:
			self.x = Globals.level_width - self.w
		if self.y < 0:
			self.y = 0
			self.momY = 0
		elif self.y > Globals.level_height:
			self.respawn()

	# Respawns the player at the most recent checkpoint
	def respawn(self):

		# Checks the player has a checkpoint
		if self.checkpoint is not None:

			# Sets the player's position
			self.x = self.checkpoint.x + int(self.checkpoint.w / 2)
			self.y = (self.checkpoint.y + self.checkpoint.h) - (self.h * (3/2))

			# Resets the player's attributes
			self.is_blinking = True
			self.blink_start_time = time.time()
			self.tool = None

			# Sets misc attributes
			self.is_grounded = False
			self.momY = 0
		else:
			raise Exception("Player has no checkpoint")

	# Decides whether the player should respawn or lose his tool
	def on_hit(self):

		# Checks if the player is still recovering
		if not time.time() - self.blink_start_time <= self.recover_delay:

			# Decides whether to respawn or lose tool
			if self.tool is None:
				self.respawn()
			else:
				self.tool = None
				self.sprite_indexes = [1]
				self.last_blink = time.time()
				self.is_blinking = True
				self.blink_start_time = time.time()
				self.using_tool = False

	# Moves the camera to follow the player
	def move_camera(self):

		# Decides whether to move the camera
		if self.x >= Globals.window.get_size()[0] / 2:
			Globals.camera_offset['x'] = - (self.x - Globals.window.get_size()[0] / 2)
		else:
			Globals.camera_offset['x'] = 0

		Globals.camera_offset['y'] = (Globals.window.get_size()[1] / 2) - self.y

		if Globals.camera_offset['y'] > 0:
			Globals.camera_offset['y'] = 0
		# if self.y - Globals.camera_offset['y'] >= Globals.window.get_size()[1] * (3/4) and self.momY < 150:
		# 	Globals.camera_offset['y'] = - (self.y - Globals.window.get_size()[1] * (3/4))
		# elif self.y - Globals.camera_offset['y'] < Globals.window.get_size()[1] * (1/4):
		# 	Globals.camera_offset['y'] = - (self.y - Globals.window.get_size()[1] * (1/4))

	# Creates the blinking animation used when the player is hit
	def blink(self): 

		# Checks if the player is blinking
		if self.is_blinking:

			# Checks whether player should show/not show
			if time.time() - self.last_blink >= self.blink_delay:
				self.last_blink = time.time()
				self.is_showing = not self.is_showing

			# Checks whether the player should stop blinking
			if time.time() - self.blink_start_time >= self.recover_delay:
				self.is_blinking = False
				self.is_showing = True

	# Animates the player's arms when using a tool
	# Tools are animated by the tool sprite
	def animate_tool(self):

		# Checks that the player is using their tool tool
		if self.using_tool:

			# Depending on the tool, animates the player
			if self.tool == "Bow and Arrow":

				# Sets the animation based on how much time has passed
				self.sprite_indexes = [3]
				t = time.time() - self.tool_time
				self.arrow_speed = t * 40
				if self.arrow_speed > 40:
					self.arrow_speed = 40

				if t > 0.5:
					self.sprite_indexes = [4]

					if t > 1:
						self.sprite_indexes = [5]

			elif self.tool == "Sword" or self.tool == "Staff":

				# Swings the player's arms
				t = time.time() - self.tool_time
				self.sprite_indexes = [6]

				if t > 0.1:
					self.sprite_indexes = [7]

					if t > 0.2:
						self.sprite_indexes = [8]

						if self.tool == "Sword":
							self.use_tool()

						if t > 0.3:
							self.sprite_indexes = [9]

							if t > 0.4:
								if self.tool == "Staff":
									self.use_tool()

								self.using_tool = False
								self.sprite_indexes = [0, 1, 2, 1]

	# Ran every frame
	# Runs the function that need to be called every frame
	def update(self):

		self.move()
		self.animate_tool()
		self.move_camera()

		self.blink()

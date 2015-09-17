from assets.files.entities.jumping_entity import JumpingEntity
from assets.files.utilities.globals import Globals

from assets.files.entities.projectiles.arrow import Arrow

import time
import pygame

class Player (JumpingEntity):

	x_translate = 0
	speed = 300

	jump_strength = 13
	momY = 0
	is_grounded = True

	last_time = 0
	delta_time = 0

	last_move_time = 0

	last_hit = 0
	recover_delay = 3

	is_dead = None
	
	tool = None

	def __init__(self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size
		self.w = self.make_pixelated(10)
		self.h = self.make_pixelated(19)

		self.is_dead = False

		self.tool = None

		self.jump_strength *= Globals.block_size

		self.sprites = [
			pygame.image.load("assets/images/player/run_1.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_2.png").convert_alpha(),
			pygame.image.load("assets/images/player/run_3.png").convert_alpha(),

			#Bow and arrow
			pygame.image.load("assets/images/player/bar_1.png"),
			pygame.image.load("assets/images/player/bar_2.png"),
			pygame.image.load("assets/images/player/bar_3.png")
		]

		self.sprite_indexes = [
			1
		]

		self.no_tool_sprite_indexes = [0, 1, 2, 1]

		self.jump_last_time = time.time()

		self.is_animated = True
		self.sprite_interval = 100

		self.last_move_time = time.time()

	def while_keys_down (self, keys):

		if self.tool == "Bow and Arrow":

			idle_sprites = [4]
			running_sprites = [3, 4, 5, 4]

		else:
			idle_sprites = [1]
			running_sprites = [0, 1, 2, 1]

		if pygame.K_LEFT in keys or pygame.K_RIGHT in keys:
			self.sprite_indexes = running_sprites

			if pygame.K_LEFT in keys:

				self.x_translate = -1
				self.facing_left = True

			if pygame.K_RIGHT in keys:

				self.x_translate = 1
				self.facing_left = False

		if pygame.K_RIGHT not in keys and pygame.K_LEFT not in keys:

			self.x_translate = 0
			self.sprite_indexes = idle_sprites

		if pygame.K_UP in keys and self.is_grounded:

			self.start_jump()

		if pygame.K_SPACE in keys:

			self.use_tool()

	def use_tool (self):

		if self.tool == "Bow and Arrow":

			if self.facing_left:
				x = self.x
				direction = -1

			else:
				x = self.x + self.h
				direction = 1
		
			Globals.projectiles.append(Arrow(x=x, y=self.y + int(self.h / 2), direction=direction, is_enemy=False))


	def move (self):

		self.x += self.x_translate * self.speed * self.delta_time

		for enemy in Globals.enemies:

			if self.check_for_collision(enemy):

				self.on_hit()

	def respawn (self):

		if not self.checkpoint == None:

			self.x = self.checkpoint.x + int(self.checkpoint.w / 2)
			self.y = self.checkpoint.y - 2 * Globals.block_size

			self.is_grounded = False

			self.momY = 0

	def on_hit (self):

		if time.time() - self.last_hit >= self.recover_delay:

			if self.tool == None:

				self.respawn()
			else:
				self.tool = None
				self.sprite_indexes = [1]
				self.last_hit = time.time()


	def update (self):

		self.set_delta_time()

		self.move()

		if self.x >= Globals.window.get_size()[0] / 2:

			Globals.camera_offset['x'] = - (self.x - Globals.window.get_size()[0] / 2)

		else:
			Globals.camera_offset['x'] = 0

		self.gravity_update()

		self.render()
from assets.files.entities.jumping_entity import JumpingEntity
from assets.files.utilities.globals import Globals

from assets.files.entities.projectiles.arrow import Arrow
from assets.files.utilities.hitbox import Hitbox

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

	using_tool = False
	bow_draw_time = 0

	last_hit = 0
	recover_delay = 3

	is_blinking = False
	last_blink = 0
	blink_delay = 0.1
	is_showing = True

	is_dead = None
	checkpoint = None

	
	tool = None

	def __init__(self, x, y):

		self.is_dead = False

		self.tool = None

		self.jump_strength *= Globals.block_size

		self.graphic_sprites = [

			#8-bit
			[
				self.img_load("player/run_1.png"),
				self.img_load("player/run_2.png"),
				self.img_load("player/run_3.png"),

				#Bow and arrow
				self.img_load("player/bar_1.png"),
				self.img_load("player/bar_2.png"),
				self.img_load("player/bar_3.png"),

				self.img_load("player/bar_shoot_1.png"),
				self.img_load("player/bar_shoot_2.png"),
				self.img_load("player/bar_shoot_full.png"),

				#sword
				self.img_load("player/sword_1.png"),
				self.img_load("player/sword_2.png"),
				self.img_load("player/sword_3.png"),

				self.img_load("player/sword_attack_1.png"),
				self.img_load("player/sword_attack_2.png"),
				self.img_load("player/sword_attack_3.png"),
				self.img_load("player/sword_attack_4.png")
			],
			#16-bit
			[

				self.img_load("player/16_run_1.png"),
				self.img_load("player/16_run_2.png"),
				self.img_load("player/16_run_3.png"),

				self.img_load("player/16_bar_1.png"),
				self.img_load("player/16_bar_2.png"),
				self.img_load("player/16_bar_3.png"),

				#bar

				self.img_load("player/16_bar_shoot_1.png"),
				self.img_load("player/16_bar_shoot_2.png"),
				self.img_load("player/16_bar_shoot_full.png"),

				#sword
				self.img_load("player/16_sword_1.png"),
				self.img_load("player/16_sword_2.png"),
				self.img_load("player/16_sword_3.png"),

				self.img_load("player/16_sword_attack_1.png"),
				self.img_load("player/16_sword_attack_2.png"),
				self.img_load("player/16_sword_attack_3.png"),
				self.img_load("player/16_sword_attack_4.png")

			]
		]

		self.sprites = self.graphic_sprites[0]

		self.graphics_addon = 6

		self.sprite_indexes = [
			1
		]

		self.no_tool_sprite_indexes = [0, 1, 2, 1]

		self.jump_last_time = time.time()

		self.is_animated = True
		self.sprite_interval = 100

		self.last_move_time = time.time()

		self.entity_init(x, y)

		self.hitboxes = []

		self.add_hitbox(x=10,y=0,w=10,h=12)
		self.add_hitbox(x=12, y=12, w=6, h=7)
		

		self.is_showing = True

	def while_keys_down (self, keys):

		if pygame.K_LEFT in keys or pygame.K_RIGHT in keys:

			if pygame.K_LEFT in keys:

				self.x_translate = -1
				self.facing_left = True

			if pygame.K_RIGHT in keys:

				self.x_translate = 1
				self.facing_left = False

		if pygame.K_RIGHT not in keys and pygame.K_LEFT not in keys:

			self.x_translate = 0

		if pygame.K_UP in keys and self.is_grounded and not self.using_tool:

			self.start_jump()

		if pygame.K_SPACE in keys:

			if self.tool == "Bow and Arrow":

				if not self.using_tool:
					self.bow_draw_time = time.time()

				self.using_tool = True

			elif self.tool == "Sword":

				self.sword_time = time.time()

				self.using_tool = True

		elif self.using_tool and self.tool == "Bow and Arrow":

			self.use_tool()

	def use_tool (self):

		if self.tool == "Bow and Arrow":

			if self.facing_left:
				x = self.x
				direction = -1

			else:
				x = self.x + self.w
				direction = 1
		
			Globals.projectiles.append(Arrow(x=self.x + (self.w / 2), y=self.y + int(self.h * (3/5)), direction=direction, is_enemy=False, speed=self.arrow_speed))

			self.using_tool = False

		elif self.tool == "Sword":

			pass


	def move (self):

		if self.tool == "Bow and Arrow":

			idle_sprites = [4]
			running_sprites = [3, 4, 5, 4]

		elif self.tool == "Sword":

			idle_sprites = [10]
			running_sprites = [10, 11, 10, 9]

		else:
			idle_sprites = [1]
			running_sprites = [0, 1, 2, 1]

		if not self.using_tool:
			self.x += self.x_translate * self.speed * self.delta_time

			if self.x_translate == 0:
				self.sprite_indexes = idle_sprites

			else:
				self.sprite_indexes = running_sprites

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
				self.last_blink - time.time()
				self.is_blinking = True
				self.blink_start_time = time.time()

	def move_camera (self):

		if self.x >= Globals.window.get_size()[0] / 2:

			Globals.camera_offset['x'] = - (self.x - Globals.window.get_size()[0] / 2)

		else:
			Globals.camera_offset['x'] = 0

	def blink(self): 

		if self.is_blinking:
			if time.time() - self.last_blink >= self.blink_delay:
				self.last_blink = time.time()
				self.is_showing =  not self.is_showing

			if time.time() - self.last_hit >= self.recover_delay:
				self.is_blinking = False
				self.is_showing = True

	def animate_tool (self):

		if self.using_tool:

			if self.tool == "Bow and Arrow":

				self.sprite_indexes = [6]

				t = time.time() - self.bow_draw_time

				self.arrow_speed = 2

				if t > 0.5:

					self.arrow_speed = 20

					self.sprite_indexes = [7]

					if t > 1:

						self.arrow_speed = 40

						self.sprite_indexes = [8]
			elif self.tool == "Sword":

				t = time.time() - self.sword_time
				self.sprite_indexes = [12]

				if t > 0.1:

					self.sprite_indexes = [13]

					if t > 0.2:

						self.sprite_indexes = [14]

						if t > 0.3: 

							self.sprite_indexes = [15]

							if t > 0.4:

								self.using_tool = False


	def update (self):

		self.move()

		self.animate_tool()

		self.move_camera()

		self.blink()
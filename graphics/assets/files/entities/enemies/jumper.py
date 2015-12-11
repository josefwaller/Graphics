from assets.files.entities.enemies.smart_enemy import SmartEnemy
from assets.files.utilities.globals import Globals

import time

class Jumper (SmartEnemy):

	last_jump_time = 0
	was_landed = False
	jump_delay = 0
	recoil_delay = 0
	x_translate = 0

	def __init__(self, x, y):

		self.is_animated = True

		self.graphic_sprites = [
			[
				self.img_load("enemies/jumper/t_jumper_jump.png"),
				self.img_load("enemies/jumper/t_jumper_land.png")
			],
			[
				self.img_load("enemies/jumper/jumper_jump.png"),
				self.img_load("enemies/jumper/jumper_land.png")
			],
			[
				self.img_load("enemies/jumper/16_jumper_jump.png"),
				self.img_load("enemies/jumper/16_jumper_land.png")
			]
		]

		self.sprites = self.graphic_sprites[0]

		self.sprite_indexes = [0, 1]
		self.sprite_interval = 500

		self.idle_indexes = [0, 1]
		self.attack_indexes = [0]
		self.land_indexes = [1]

		self.visible_range = 20 * Globals.block_size
		self.attack_duration = 1
		self.attack_delay = 1
		self.speed = 50 * Globals.block_size
		self.jump_strength = 13 * Globals.block_size

		self.landing_pause = 5
		self.landing_time = 0

		self.hitboxes = []
		self.add_hitbox(x=8, y=1, w=5, h=12)

		self.h = 16
		self.w = 24

		self.entity_init(x, y)
		self.last_jump = time.time()
		self.momY = 0

	def attack (self):
		if self.is_grounded:

			self.sprite_indexes = self.land_indexes

			if time.time() - self.landing_time >= self.landing_pause:

				if self.facing_left:
					self.x_translate = 1

				else:
					self.x_translate = -1

				self.speed = abs(Globals.player.x - self.x) * 0.5

				self.start_jump()

				self.landing_time = time.time()
		else:

			self.x += (self.speed * self.x_translate) * self.delta_time

			self.sprite_indexes = self.attack_indexes

	def update(self):

		self.should_attack()
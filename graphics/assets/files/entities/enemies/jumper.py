from assets.files.entities.enemies.smart_enemy import SmartEnemy
from assets.files.utilities.globals import Globals

import time

class Jumper (SmartEnemy):

	last_jump_time = 0
	was_landed = False
	jump_delay = 0
	recoil_delay = 0

	def __init__(self, x, y):

		self.is_animated = True

		self.sprites = [
			self.img_load("enemies/jumper/jumper_stand_1.png"),
			self.img_load("enemies/jumper/jumper_stand_2.png"),

			self.img_load("enemies/jumper/jumper_jump.png"),
			self.img_load("enemies/jumper/jumper_land.png")
		]

		self.sprite_indexes = [0, 1]
		self.sprite_interval = 500

		self.idle_indexes = [0, 1]
		self.attack_indexes = [2]
		self.land_indexes = [3]

		self.visible_range = 20 * Globals.block_size
		self.attack_duration = 1
		self.attack_delay = 1
		self.speed = 10 * Globals.block_size
		self.jump_strength = 13 * Globals.block_size

		self.landing_pause = 2000

		self.entity_init(x, y)
		self.last_jump = time.time()

		self.set_delta_time()
		self.momY = 0

	def attack (self):
		pass


	def update (self):

		self.set_delta_time()

		direction = 0

		if self.should_attack():
			if self.facing_left:
				direction = -1
			else:
				direction = 1

			self.start_jump()

		
		self.momX = self.speed * direction

		self.x += self.momX * self.delta_time

		self.gravity_update()


		self.render()
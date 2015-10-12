from assets.files.utilities.globals import Globals
from assets.files.entities.enemies.smart_enemy import SmartEnemy
from assets.files.entities.projectiles.arrow import Arrow

import time
import pygame

class Archer (SmartEnemy):

	last_arrow_time = None
	arrow_delay = None

	is_attacking = None
	attack_duration = None

	def __init__ (self, x, y):

		self.last_attack_time = time.time()

		self.graphic_sprites = [

			[

				self.img_load("enemies/archer/archer_1.png"),
				self.img_load("enemies/archer/archer_2.png"),
				self.img_load("enemies/archer/archer_shoot.png")

			],
			[
				self.img_load("enemies/archer/16_archer_1.png"),
				self.img_load("enemies/archer/16_archer_2.png"),
				self.img_load("enemies/archer/16_archer_shoot.png")
			]

		]

		self.sprites = self.graphic_sprites[0]

		self.is_animated = True

		self.idle_indexes = [2]
		self.attack_indexes = [0,1]

		self.sprite_indexes = self.idle_indexes
		self.sprite_interval = 300

		self.last_attack_time = time.time()
		self.attack_delay = 0.1
		self.is_attacking = False
		self.attack_duration = 1

		self.visible_range = 10 * Globals.block_size

		self.hitboxes = []
		self.add_hitbox(x=3, y=2, w=7, h=6)
		self.add_hitbox(x=4, y=7, w=4, h=8)

		self.entity_init(x, y)

	def attack (self):

		if self.facing_left:
			direction = 1
		else:
			direction = -1

		Globals.projectiles.append(Arrow(x=self.x, y=self.y + int(self.h / 2), direction=direction, is_enemy=True))
		self.end_attack()

	def update (self):

		self.set_delta_time()

		self.should_attack()

		self.gravity_update()

		self.check_for_player_collision()

		self.render()


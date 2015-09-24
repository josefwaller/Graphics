from assets.files.utilities.globals import Globals
from assets.files.entities.enemies.base_ranged import BaseRanged
from assets.files.entities.projectiles.arrow import Arrow

import time
import pygame

class Archer (BaseRanged):

	last_arrow_time = None
	arrow_delay = None

	is_attacking = None
	attack_duration = None

	def __init__ (self, x, y):

		self.last_attack_time = time.time()

		self.sprites = [

			pygame.image.load("assets/images/enemies/archer/archer_1.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/archer/archer_2.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/archer/archer_shoot.png").convert_alpha()

		]

		self.is_animated = True

		self.idle_indexes = [2]
		self.attack_indexes = [0,1]

		self.sprite_indexes = self.idle_indexes

		self.sprite_indexes = self.attack_indexes
		self.sprite_interval = 300

		self.last_attack_time = time.time()
		self.attack_delay = 0.2
		self.is_attacking = False
		self.attack_duration = 2

		self.visible_range = 10 * Globals.block_size

		self.entity_init(x, y)

	def attack (self):

		if self.should_attack():

			if self.facing_left:
				direction = 1
			else:
				direction = -1

			Globals.projectiles.append(Arrow(x=self.x, y=self.y + int(self.h / 2), direction=direction, is_enemy=True))


	def update (self):

		self.set_delta_time()

		self.attack()

		self.gravity_update()

		self.check_for_player_collision()

		self.render()


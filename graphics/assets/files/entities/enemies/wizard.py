from assets.files.entities.enemies.base_enemy import BaseEnemy
from assets.files.entities.enemies.base_ranged import BaseRanged

from assets.files.entities.projectiles.missile import Missile

from assets.files.utilities.globals import Globals

import time
import pygame

class Wizard (BaseRanged):

	def __init__(self, x, y, time_offset=0, missile_delay=1):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.last_missile_time = time.time() + (time_offset * 1000)
		self.missile_delay = missile_delay
		self.missiles = []
		self.visible_range = 10 * Globals.block_size

		self.sprites = [
			pygame.image.load("assets/images/enemies/wizard/front1.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/wizard/front2.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/wizard/side.png").convert_alpha()
		]

		self.is_animated = True
		
		self.attack_indexes = [2]
		self.idle_indexes = [0, 1]

		self.sprite_indexes = self.idle_indexes
		self.sprite_interval = 100

		self.attack_duration = 1

		self.attack_delay = 1

		self.w = Globals.block_size
		self.h = Globals.block_size

	def attack (self):

		if self.should_attack():

			if self.facing_left:
				direction = 1
			else:
				direction = -1

			Globals.projectiles.append(Missile(x=self.x, y=self.y + int(4*self.h/5) , direction=direction, is_enemy=True))


	def update (self):

		self.attack()
		self.check_for_player_collision()

		self.render()
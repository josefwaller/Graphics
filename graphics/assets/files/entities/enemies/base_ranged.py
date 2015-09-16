from assets.files.entities.enemies.base_enemy import BaseEnemy
from assets.files.utilities.globals import Globals

import time

class BaseRanged (BaseEnemy):

	is_attacking = False
	idle_indexes = None
	last_attack_time = 0
	attack_duration = 0


	def should_attack (self):

		if self.is_attacking:

			if time.time() - self.attack_time >= self.attack_duration:

				self.is_attacking = False
				self.facing_left = False
				self.sprite_indexes = self.idle_indexes

				self.last_attack_time = time.time()

		else:

			if Globals.player.x > self.x:
				self.facing_left = True

			else:
				self.facing_left = False

			if time.time() - self.last_attack_time >= self.attack_duration:

				self.sprite_indexes = self.attack_indexes

				self.attack_time = time.time()
				self.is_attacking = True

				return True
		return False
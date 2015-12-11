from assets.files.entities.enemies.base_enemy import BaseEnemy
from assets.files.utilities.globals import Globals

import time


class SmartEnemy (BaseEnemy):

	is_attacking = False
	idle_indexes = None
	last_attack_time = 0
	attack_duration = 0
	attack_delay = 0
	attack_time = 0
	attack_indexes = None
	is_ending_attack = True
	visible_range = 0

	def should_attack(self):

		if self.check_visibility():

			if self.is_attacking:

				if Globals.player.x > self.x:
					self.facing_left = True

				else:
					self.facing_left = False

				if self.is_ending_attack:

					if time.time() - self.attack_time >= self.attack_duration:

						self.is_attacking = False
						self.sprite_indexes = self.idle_indexes
						self.is_ending_attack = False
						self.last_attack_time = time.time()

				else:

					self.attack()

			else:

				if time.time() - self.last_attack_time > self.attack_delay:
					
					self.sprite_indexes = self.attack_indexes

					self.is_attacking = True

					return True
					
		return False

	def check_visibility(self):

		visible_x = False
		visible_y = False

		if Globals.player.x + Globals.player.w > self.x - self.visible_range:
			if Globals.player.x < self.x + self.w + self.visible_range:
				visible_x = True

		if Globals.player.y + Globals.player.h > self.y - self.visible_range:
			if Globals.player.y < self.y + self.h + self.visible_range:
				visible_y = True
		if visible_x and visible_y:
			return True
		else:
			return False

	def end_attack(self):

		self.is_ending_attack = True

		self.attack_time = time.time()
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
	visible_range_x = None
	visible_range_y = None

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
		range_x = 0
		range_y = 0
		
		if self.visible_range_x is None and self.visible_range_y is None:
			range_x = self.visible_range
			range_y = self.visible_range
		else:
			range_x = self.visible_range_x
			range_y = self.visible_range_y

		if Globals.player.x + Globals.player.w > self.x - range_x:
			if Globals.player.x < self.x + self.w + range_x:
				visible_x = True

		if Globals.player.y + Globals.player.h > self.y - range_y:
			if Globals.player.y < self.y + self.h + range_y:
				visible_y = True
		if visible_x and visible_y:
			return True
		else:
			return False

	def end_attack(self):

		self.is_ending_attack = True

		self.attack_time = time.time()
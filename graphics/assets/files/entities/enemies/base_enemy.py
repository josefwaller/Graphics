from assets.files.entities.jumping_entity import JumpingEntity
from assets.files.utilities.globals import Globals

import random
import time
import pygame


class BaseEnemy (JumpingEntity):

	death_spin_speed = 0
	death_push_speed = 0

	death_time = 0

	death_speed_x = 0

	death_sprite = None

	momY = 0

	def check_for_player_collision(self):

		if not self.is_dying:

			collide_x = False
			collide_y = False

			for hb in Globals.player.hitboxes:

				if self.x < hb.x + hb.w:
					if self.x + self.w > hb.x:

						collide_x = True

				if self.y < hb.y + hb.w:
					if self.y + self.h > hb.y:

						collide_y = True

				if collide_x and collide_y:
					Globals.player.on_hit()

	def on_hit(self):

		if not self.is_dying:

			if random.random() > 0.5:
				direction = 1
			else:
				direction = -1

			self.is_dying = True
			self.death_time = time.time()
			self.momY = (random.random() * 10) + 5
			self.death_spin_speed = (random.random() * 90) + 180
			self.death_speed_x = (random.random() * 200) + 300 * direction
			self.momY = -400
			self.death_sprite = self.sprites[self.sprite_indexes[self.this_index]]

			self.sprites = [self.death_sprite]
			self.sprite_indexes = [0]
			self.this_index = 0

	def death_animation(self):

		time_since = time.time() - self.death_time

		self.sprites[0] = pygame.transform.rotate(self.death_sprite, self.death_spin_speed * time_since)

		self.x += self.death_speed_x * self.delta_time

		self.momY += (3 * Globals.gravity_strength) * self.delta_time
		self.y += self.momY * self.delta_time

		if self.y + Globals.camera_offset['y'] > Globals.window.get_size()[1]:
			self.remove_self()

	def remove_self(self):
		if self in Globals.enemies:
			Globals.enemies.remove(self)



from assets.files.utilities.globals import Globals
from assets.files.entities.projectiles.base_projectile import BaseProjectile

import time
import pygame

class Arrow (BaseProjectile):

	def __init__ (self, x, y, direction, is_enemy=True, speed=20):

		self.speed = speed * Globals.block_size

		self.graphic_images = [
			self.img_load("enemies/archer/arrow.png"),
			self.img_load("enemies/archer/16_arrow.png")
		]

		self.image = self.graphic_images[0]

		self.direction = direction

		self.is_enemy = is_enemy
		
		self.add_hitbox(x=0, y=0, h=2, w=6)

		self.is_static = False
		self.is_animated = False

		if self.direction == 1:
			self.facing_left = True

		else:
			self.facing_left = False

		self.entity_init(x, y)

		self.x = x
		self.y = y

	def move (self):

		self.x += self.speed * self.delta_time * self.direction

		if self.is_grounded:

			Globals.projectiles.remove(self)
			return

		if self.is_enemy:
			if self.check_for_collision(Globals.player):
				Globals.player.on_hit()
		else:
			for enemy in Globals.enemies:
				if self.check_for_collision(enemy):
					Globals.enemies.remove(enemy)
					Globals.projectiles.remove(self)
					return

	def update (self):

		self.move()
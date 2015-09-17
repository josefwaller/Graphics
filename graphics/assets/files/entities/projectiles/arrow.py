from assets.files.utilities.globals import Globals
from assets.files.entities.jumping_entity import JumpingEntity

import time
import pygame

class Arrow (JumpingEntity):

	def __init__ (self, x, y, direction, is_enemy=True):

		self.x = x
		self.y = y

		self.speed = 20 * Globals.block_size

		self.w = self.make_pixelated(6)
		self.h = self.make_pixelated(3)

		self.image = pygame.image.load("assets/images/enemies/archer/arrow.png").convert_alpha()

		self.direction = direction

		self.is_enemy = is_enemy

		if self.direction == 1:
			self.facing_left = True

		else:
			self.facing_left = False

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

		self.set_delta_time()

		self.move()

		self.gravity_update()

		self.render()
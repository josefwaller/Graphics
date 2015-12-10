from assets.files.utilities.globals import Globals
from assets.files.entities.projectiles.base_projectile import BaseProjectile


class Arrow (BaseProjectile):

	last_x = 0
	last_y = 0

	def __init__(self, x, y, direction, is_enemy=True, speed=20):

		self.speed = speed * Globals.block_size

		self.graphic_images = [
			self.img_load("enemies/archer/t_arrow.png"),
			self.img_load("enemies/archer/arrow.png"),
			self.img_load("enemies/archer/16_arrow.png")
		]

		self.image = self.graphic_images[0]

		self.direction = direction

		self.is_enemy = is_enemy
		self.w, self.h = 6, 2
		self.add_hitbox(x=0, y=0, w=6, h=2)

		self.is_static = False
		self.is_animated = False

		if self.direction == 1:
			self.facing_left = True

		else:
			self.facing_left = False

		self.entity_init(x, y)

		self.x = x
		self.y = y

		self.last_x = x

	def move(self):

		self.x += self.speed * self.delta_time * self.direction

	def update(self):

		self.move()

		self.check_for_player()

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
		self.last_y = y

	def move(self):

		self.x += self.speed * self.delta_time * self.direction

	# Checks if it hit the side of a platform
	# Needed because base entity will just move it over, instead of removing the entity
	def check_for_horizontal_collision(self):

		for p in Globals.platforms:
			if p.y < self.y + self.h:
				if p.y + p.h > self.y:
					if p.x < self.x + self.w:
						if p.x + p.w > self.x:
							self.remove_self()

	def update(self):

		self.move()
		self.check_for_horizontal_collision()

		if self.is_grounded:
			self.remove_self()

		if self.check_for_target():
			Globals.player.on_hit()
			self.remove_self()

	def check_for_target(self):

		if self.is_enemy:
			if self.check_for_missed_collision(Globals.player):
				Globals.player.on_hit()
		else:
			for enemy in Globals.enemies:
				if self.check_for_missed_collision(enemy):
					enemy.on_hit()
					break

	def check_for_missed_collision(self, target):
		# Checks if it is in the player first
		if self.check_for_collision(target):
			return True

		# Checks if both this frame and last frame where in line with the player
		collide_y = False

		if self.y + self.h > target.y:
			if self.y < target.y + target.h:
				if self.last_y + self.h > target.y:
					if self.last_y < target.y + target.h:
						collide_y = True

		# Checks to see if the arrow went through the player this frame
		if collide_y:
			if self.direction == 1:
				if target.x < self.x + self.w:
					if target.x + target.w > self.last_x:
						return True
			else:
				if target.x < self.x:
					if target.x + target.w > self.last_x:
						return True


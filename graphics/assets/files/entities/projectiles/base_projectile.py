from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals


class BaseProjectile (BaseEntity):

	is_enemy = True

	def check_for_target(self):

		if self.is_enemy:

			if self.check_for_collision(Globals.player):
				Globals.player.on_hit()
				Globals.projectiles.remove(self)

		else:

			for enemy in Globals.enemies:
				if self.check_for_collision(enemy):
					enemy.on_hit()
					self.remove_self()
					break

		if self.is_grounded:
			if self in Globals.projectiles:
				self.remove_self()
				return

		for platform in Globals.platforms:
			if self.check_for_collision(platform):
				self.remove_self()
				break

	def remove_self(self):
		if self in Globals.projectiles:
			Globals.projectiles.remove(self)

from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

class BaseProjectile (BaseEntity):

	is_enemy = True

	def check_for_player (self):

		if self.is_enemy:

			if self.check_for_collision(Globals.player):
				Globals.player.on_hit()
				Globals.projectiles.remove(self)

		else:

			for enemy in Globals.enemies:
				if self.check_for_collision(enemy):
					enemy.on_hit()
					Globals.projectiles.remove(self)
					break


		for platform in Globals.platforms:
			if self.check_for_collision(platform):
				Globals.projectiles.remove(self)
				break
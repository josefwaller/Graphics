from assets.files.entities.jumping_entity import JumpingEntity
from assets.files.utilities.globals import Globals

class BaseEnemy (JumpingEntity):

	def check_for_player_collision (self):

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

	def on_death (self):

		Globals.enemies.remove(self)

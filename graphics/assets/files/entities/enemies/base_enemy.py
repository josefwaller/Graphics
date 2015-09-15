from assets.files.entities.jumping_entity import JumpingEntity
from assets.files.utilities.globals import Globals

class BaseEnemy (JumpingEntity):

	def check_for_player_collision (self):

		collide_x = False
		collide_y = False

		player = Globals.player

		if self.x < player.x + player.w:
			if self.x + self.w > player.x:

				collide_x = True

		if self.y < player.y + player.h:
			if self.y + self.h > player.y:

				collide_y = True

		if collide_x and collide_y:

			Globals.player.is_alive = False

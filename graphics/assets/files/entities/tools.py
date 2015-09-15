from assets.files.entities import BaseEntity
from assets.files.utilities import Globals

class BowAndArrow (BaseEntity):

	def __init__ (self):

		self.w = Globals.block_size
		self.h = Globals.block_size

	def check_for_player (self):

		player = Globals.player

		if player.x < self.x + self.w:
			if player.x + player.w > self.x:

				if player.y < self.y + self.h:
					if player.y + player.h > self.y:

						Player.tool = "Bow and Arrow"

	def update (self):

		self.set_delta_time()

		self.check_for_player
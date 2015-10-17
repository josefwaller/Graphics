from assets.files.utilities.globals import Globals
from assets.files.entities.base_entity import BaseEntity

class BaseTool (BaseEntity):

	def tool_init (self):
		
		self.w = Globals.block_size
		self.h = Globals.block_size

		self.image = self.graphic_images[0]
		self.facing_left = False

	def check_for_player (self):

		player = Globals.player

		if self.check_for_collision(player):		

			player.tool = self.tool_name

	def update (self):

		self.check_for_player()
from assets.files.utilities.globals import Globals
from assets.files.entities.base_entity import BaseEntity


class BaseTool (BaseEntity):

	def tool_init (self):

		self.image = self.graphic_images[0]
		self.facing_left = False

		self.is_animated = False

		self.is_static = True
		
		self.w = Globals.block_size
		self.h = Globals.block_size

		self.resize_images()

		self.clip_to_hitboxes()

	def check_for_player (self):

		player = Globals.player

		if self.check_for_collision(player) and player.is_blinking is False:

			player.tool = self.tool_name

	def update (self):

		self.check_for_player()
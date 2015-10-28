from assets.files.entities.tools.base_tool import BaseTool
from assets.files.utilities.globals import Globals

class BowAndArrow (BaseTool):

	def __init__ (self, x, y):

		self.is_tool = True

		self.graphic_images = [
			self.img_load("tools/bar.png"),
			self.img_load("tools/16_bar.png")
		]

		self.tool_init()

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.clip_to_hitboxes()
		self.tool_name = "Bow and Arrow"

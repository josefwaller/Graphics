from assets.files.entities.tools.base_tool import BaseTool
from assets.files.utilities.globals import Globals

class Sword (BaseTool):

	def __init__(self, x, y):

		self.graphic_images = [
			self.img_load("tools/sword.png"),
			self.img_load("tools/sword.png")
		]
		self.image = self.graphic_images[0]

		self.tool_init()

		self.entity_init(0, 0)

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.tool_name = "Sword"
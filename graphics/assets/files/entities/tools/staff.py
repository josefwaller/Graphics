from assets.files.entities.tools.base_tool import BaseTool
from assets.files.utilities.globals import Globals


class Staff (BaseTool):

	def __init__(self, x, y):

		self.graphic_images = [
			self.img_load("tools/t_staff.png"),
			self.img_load("tools/staff.png"),
			self.img_load("tools/staff.png")
		]
		self.image = self.graphic_images[0]

		self.tool_init()

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.tool_name = "Staff"

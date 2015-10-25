from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

class EndBlock (BaseEntity):

	def __init__(self, x, y, num):

		self.graphic_images = [

			self.img_load("blocks/up_graphics_16.png"),
			self.img_load("blocks/16_up_graphics_16.png")

		]
		self.image = self.graphic_images[0]

		self.is_animated = False

		self.facing_left = True

		self.num = num

		self.used = False

		self.add_hitbox(0, 0, 1, 1)

		self.entity_init(x, y)

		self.update_graphics()

	def update(self):

		if self.check_for_collision(Globals.player) and not self.used:
			return
			
			Globals.graphics_level += 1

			Globals.is_paused = True

			Globals.pop_up_m.show_message("You now have sixteen bit graphics")

			self.update_graphics()

			self.used = True
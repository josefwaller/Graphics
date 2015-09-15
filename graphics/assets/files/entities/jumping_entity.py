import time

from .base_entity import BaseEntity
from assets.files.utilities.globals import Globals

class JumpingEntity (BaseEntity):

	jump_strength = None
	momY = None
	is_grounded = None

	def start_jump (self):

		self.momY = self.jump_strength

		self.is_grounded = False

	def gravity_update (self):

		starting_y = self.y

		if self.is_grounded == False:

			self.momY -= Globals.gravity_strength * self.delta_time

			self.y -= self.momY * self.delta_time

			for platform in Globals.platforms:

				collide_x = False
				collide_y = False

				if self.x <= platform.x + platform.w * Globals.block_size:
					if self.x + self.w >= platform.x:

						collide_x = True

				if self.y + self.h >= platform.y :
					if starting_y + self.h < platform.y:

						collide_y = True

				if collide_x and collide_y:

					self.is_grounded = True
					self.y = (platform.y - self.h)
					self.platform_under = platform
					break
				else:
					self.is_grounded = False

		else:

			platform = self.platform_under

			if platform == None or self.x > platform.x + platform.w * Globals.block_size or self.x + self.w < platform.x:

				self.is_grounded = False
				self.momY = 0
				self.platform_under = None
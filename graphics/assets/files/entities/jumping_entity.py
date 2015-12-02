import time

from .base_entity import BaseEntity
from assets.files.utilities.globals import Globals

class JumpingEntity (BaseEntity):

	jump_strength = None
	is_grounded = None
	is_static = False

	def start_jump (self):

		if self.is_grounded:

			self.momY = self.jump_strength

			self.is_grounded = False

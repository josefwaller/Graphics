from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import pygame
import time

class BowAndArrow (BaseEntity):

	def __init__ (self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.image = pygame.image.load("assets/images/blocks/temp_block.png").convert_alpha()

		self.w = Globals.block_size
		self.h = Globals.block_size


	def check_for_player (self):

		player = Globals.player

		if self.check_for_collision(player):		

			player.tool = "Bow and Arrow"

	def update (self):

		self.set_delta_time()

		self.check_for_player()

		self.render()
from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import pygame
import time

class BowAndArrow (BaseEntity):

	def __init__ (self, x, y):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.image = self.img_load("tools/bar.png")
		self.facing_left = False

		self.w = Globals.block_size
		self.h = Globals.block_size


	def check_for_player (self):

		player = Globals.player

		if self.check_for_collision(player):		

			player.tool = "Bow and Arrow"

			player.sprite_indexes = [3, 4, 5, 4]

	def update (self):

		self.set_delta_time()

		self.check_for_player()

		self.render()
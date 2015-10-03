from assets.files.entities.base_entity import BaseEntity
from assets.files.utilities.globals import Globals

import pygame
import time

class BowAndArrow (BaseEntity):

	def __init__ (self, x, y):

		self.image = self.img_load("tools/bar.png")
		self.facing_left = False

		self.w = Globals.block_size
		self.h = Globals.block_size

		self.entity_init(0, 0)

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size


	def check_for_player (self):

		player = Globals.player

		if self.check_for_collision(player):		

			player.tool = "Bow and Arrow"

			player.sprite_indexes = [4]

	def update (self):

		self.check_for_player()
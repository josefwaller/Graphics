from assets.files.utilities.globals import Globals
from assets.files.entities.enemies.base_enemy import BaseEnemy

import time
import pygame

class Walker (BaseEnemy):

	facing_left = False
	speed = 100

	def __init__(self, x, y, turn1, turn2, facing_left=True):
		self.facing_left = facing_left

		if turn1 > turn2:
			self.turn_one = turn2 * Globals.block_size
			self.turn_two = turn1 * Globals.block_size

		else:
			self.turn_one = turn1 * Globals.block_size
			self.turn_two = turn2 * Globals.block_size

		self.is_animated = True

		self.sprite_interval = 150

		self.last_time = time.time()

		self.sprites = [
			self.img_load("enemies/walker/run_1.png"),
			self.img_load("enemies/walker/run_2.png"),
			self.img_load("enemies/walker/run_3.png"),
			self.img_load("enemies/walker/run_2.png")
		]

		self.sprite_indexes = [
			0,
			1,
			2,
			1
		]

		self.jump_last_time = time.time()

		self.entity_init(x, y)

	def move (self):

		if self.facing_left == True:
			self.x -= self.speed * self.delta_time

		else:
			self.x += self.speed * self.delta_time

		if self.x < self.turn_one:
			self.facing_left = False

		elif self.x + self.w > self.turn_two:
			self.facing_left = True

	def update (self):

		self.set_delta_time()

		self.move()

		self.gravity_update()
		self.render()

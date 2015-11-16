from assets.files.utilities.globals import Globals
from assets.files.utilities.hitbox import Hitbox

from assets.files.entities.projectiles.base_projectile import BaseProjectile

import pygame
import time
import Math


class Missile (BaseProjectile):

	lifespan = None
	starting_time = None
	speed = None

	momX = None
	moxY = None

	def __init__(self, x, y, direction=1, is_enemy=True):
		self.lifespan = 1

		self.speed = 5

		if is_enemy:
			self.target = Globals.player
		else:
			self.target = self.find_target()

		self.starting_time = time.time()

		self.momX = 30 * direction
		self.momY = 0

		self.turn_speed = 500

		self.is_animated = False
		self.is_static = True
		self.graphic_images = [
			self.img_load("enemies/wizard/missile.png"),
			self.img_load("enemies/wizard/16_missile.png")
		]
		self.image = self.graphic_images[0]

		self.add_hitbox(x=0, y=0, w=6, h=6)

		self.entity_init(x, y)

		self.x = x
		self.y = y

	def move (self):

		x_translate = 0
		y_translate = 0

			if self.target.x > self.x + self.w:

				x_translate = 1

			elif self.target.x + self.target.w < self.x:

				x_translate = -1

			elif self.target.x + self.target.w > self.x and self.target.x < self.x + self.w:

				if self.momX > 0:
					x_translate = -1
				elif self.momX < 0:
					x_translate = 1

			if self.target.y > self.y + self.h:

				y_translate = 1

			elif self.target.y + self.target.h < self.y:

				y_translate = -1

			elif self.target.y < self.y + self.w and self.target.y + self.target.h > self.y:

				if self.momY > 0:
					y_translate = -1
				elif self.momY < 0:
					y_translate = 1

			self.momX += x_translate * self.turn_speed * self.delta_time
			self.momY += y_translate * self.turn_speed * self.delta_time

			self.x += self.momX * self.speed * self.delta_time
			self.y += self.momY * self.speed * self.delta_time

			if self.is_enemy:

				if self.check_for_collision(self.target):
					self.target.on_hit()

			if time.time() - self.starting_time >= self.lifespan:
				Globals.projectiles.remove(self)

	def find_target (self): 

		least_distance = None
		enemy = None
		
		for e in Globals.enemies:

			x = Math.abs(e.x - self.x)
			y = Math.abs(e.y - self.y)

			distance = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2))

			if distance < least_distance:
				least_distance = distance
				enemy = e

		return e

	def update (self):

		self.move()
		self.render()
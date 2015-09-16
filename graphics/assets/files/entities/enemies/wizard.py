from assets.files.entities.enemies.base_enemy import BaseEnemy
from assets.files.entities.enemies.base_ranged import BaseRanged

from assets.files.utilities.globals import Globals

import time
import pygame

class Wizard (BaseRanged):

	def __init__(self, x, y, time_offset=0, missile_delay=1):

		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		self.last_missile_time = time.time() + (time_offset * 1000)
		self.missile_delay = missile_delay
		self.missiles = []
		self.visible_range = 10 * Globals.block_size

		self.sprites = [
			pygame.image.load("assets/images/enemies/wizard/front1.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/wizard/front2.png").convert_alpha(),
			pygame.image.load("assets/images/enemies/wizard/side.png").convert_alpha()
		]

		self.is_animated = True
		
		self.attack_indexes = [2]
		self.idle_indexes = [0, 1]

		self.sprite_indexes = self.idle_indexes
		self.sprite_interval = 100

		self.attack_duration = 1

		self.w = Globals.block_size
		self.h = Globals.block_size

	def attack (self):

		if self.should_attack():

			if self.facing_left:
				direction = 1
			else:
				direction = -1

			Globals.enemies.append(Missile(x=self.x, y=self.y + int(4*self.h/5) , direction=direction))


	def update (self):

		self.attack()
		self.check_for_player_collision()

		self.render()


class Missile (BaseEnemy):

	lifespan = None
	starting_time = None
	speed = None

	momX = None
	moxY = None

	def __init__(self, x, y, direction=1):

		self.x = x
		self.y = y

		self.w = int(3 * (Globals.block_size/16))
		self.h = int(3 * (Globals.block_size/16))
		self.lifespan = 1

		self.speed = 5

		self.starting_time = time.time()

		self.momX = 30 * direction
		self.momY = 0

		self.turn_speed = 5

		self.is_animated = False
		self.image = pygame.image.load("assets/images/enemies/wizard/missile.png").convert_alpha()

	def move (self):

		x_translate = 0
		y_translate = 0

		if Globals.player.x  + Globals.player.w > self.x:

			x_translate = 1

		elif Globals.player.x < self.x + self.w:

			x_translate = -1

		if Globals.player.y > self.y:

			y_translate = 1

		elif Globals.player.y + Globals.player.h < self.y:

			y_translate = -1

		self.momX += x_translate * self.turn_speed
		self.momY += y_translate * self.turn_speed

		self.x += self.momX * self.speed * self.delta_time
		self.y += self.momY * self.speed * self.delta_time

		if time.time() - self.starting_time >= self.lifespan:
			Globals.enemies.remove(self)


	def update(self):

		self.set_delta_time()

		self.move()

		self.check_for_player_collision()

		self.render()

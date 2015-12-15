from assets.files.entities.enemies.base_enemy import BaseEnemy
from assets.files.entities.enemies.smart_enemy import SmartEnemy

from assets.files.entities.projectiles.missile import Missile

from assets.files.utilities.globals import Globals

import time
import pygame

class Wizard (SmartEnemy):

	def __init__(self, x, y, time_offset=0, missile_delay=1):

		self.last_missile_time = time.time() + (time_offset * 1000)
		self.missile_delay = missile_delay
		self.visible_range = 10 * Globals.block_size

		self.graphic_sprites = [
			[
				self.img_load("enemies/wizard/t_front_1.png"),
				self.img_load("enemies/wizard/t_front_2.png"),
				self.img_load("enemies/wizard/t_side.png")
			],
			[
				self.img_load("enemies/wizard/front_1.png"),
				self.img_load("enemies/wizard/front_2.png"),
				self.img_load("enemies/wizard/side.png")
			],
			[
				self.img_load("enemies/wizard/16_front_1.png"),
				self.img_load("enemies/wizard/16_front_2.png"),
				self.img_load("enemies/wizard/16_side.png")
			]
		]

		self.sprites = self.graphic_sprites[0]

		self.is_animated = True
		
		self.attack_indexes = [2]
		self.idle_indexes = [0, 1]

		self.sprite_indexes = self.idle_indexes
		self.sprite_interval = 100

		self.attack_duration = 1

		self.attack_delay = 2

		self.add_hitbox(x=3, y=0, w=6, h=7)
		self.add_hitbox(x=4, y=7, w=6, h=8)

		self.w = 12
		self.h = 15
		self.entity_init(x, y)

		self.missile_sound = self.load_sound("assets/sounds/missile.wav")

	def attack(self):

		if self.facing_left:
			direction = 1
		else:
			direction = -1

		Globals.projectiles.append(Missile(x=self.x, y=self.y + int(4*self.h/5) , direction=direction, is_enemy=True))
		self.missile_sound.play()
		self.end_attack()


	def update(self):

		self.should_attack()
		self.check_for_player_collision()

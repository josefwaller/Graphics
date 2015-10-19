import calendar
import time
import pygame

from assets.files.utilities.globals import Globals
from assets.files.utilities.hitbox import Hitbox

#Defualt class for everything
class BaseEntity ():
	momY = None
	is_grounded = None
	gravity_strength = None

	x = 0
	y = 0
	w = 0
	h = 0

	unix = 0

	is_animated = False

	image = None

	sprites = None
	sprite_indexes = None
	this_index = 0
	platform_under = None

	last_graphics = Globals.graphics_level

	last_sprite_time = 0
	sprite_interval = 0

	facing_left = False

	last_time = 0

	is_showing = True
	is_static = True

	def img_load(self, url):

		full_url = "assets/images/%s" % url

		image = pygame.image.load(full_url).convert_alpha()

		return image 

	def entity_init (self, x, y):

		if self.is_animated:

			self.h = self.make_pixelated(self.sprites[0].get_size()[1])
			self.w = self.make_pixelated(self.sprites[0].get_size()[0])

		else:
			self.h = self.make_pixelated(self.image.get_size()[1])
			self.w = self.make_pixelated(self.image.get_size()[0])

		self.x = x * Globals.block_size + (Globals.block_size - self.w) / 2
		self.y = y * Globals.block_size + (Globals.block_size - self.h) / 2

		try:
			self.hitboxes
		except AttributeError:
			self.hitboxes = [
				Hitbox(x=0, y=0, h=self.h, w=self.w, parent=self)
			]

	def add_hitbox (self, x, y, w, h):

		x = self.make_pixelated(x)
		y = self.make_pixelated(y)
		w = self.make_pixelated(w)
		h = self.make_pixelated(h)

		try:
			self.hitboxes
		except AttributeError:
			self.hitboxes = []

		self.hitboxes.append(Hitbox(x=x, y=y, w=w, h=h, parent=self))

	def set_delta_time(self):

		if self.last_time == 0:
			self.last_time = time.time()

		self.delta_time = (time.time() - self.last_time)

		self.last_time = time.time()

	def make_pixelated(self, num):

		return int(num * (Globals.block_size / 16))

	def check_for_collision(self, target):

		for hb in target.hitboxes:

			for shb in self.hitboxes:
				
				if hb.y + hb.h > shb.y:
					if hb.y < shb.y + shb.h:
			
						if hb.x + hb.w > shb.x:
							if hb.x < shb.x + self.w:
								return True
								break

		return False

	def base_update(self):
		self.set_delta_time()

		if not self.last_graphics == Globals.graphics_level:

			self.update_graphics()

		if not Globals.is_paused:

			if not self.is_static:
				self.gravity_update()

			self.update()

			if self.is_showing:
				self.render()

			for hb in self.hitboxes:
				hb.update()

	def render (self):

		sprite = 0

		if self.is_animated:
			self.unix = time.time() * 1000
			
			if self.last_sprite_time < self.unix - self.sprite_interval:

				self.this_index += 1
				self.last_sprite_time = time.time() * 1000

			if self.this_index >= len(self.sprite_indexes):
				self.this_index = 0

			sprite = self.sprites[self.sprite_indexes[self.this_index]]

		else:

			sprite = self.image

		sprite = pygame.transform.scale(sprite, (self.w, self.h))

		if not self.facing_left:

			sprite = pygame.transform.flip(sprite, True, False)

		Globals.window.blit(sprite, (self.x + Globals.camera_offset['x'], self.y + Globals.camera_offset['y']))

	def update_graphics (self):
				
		if self.is_animated == False:

			self.image = self.graphic_images[Globals.graphics_level]
			
		else:

			self.sprites = self.graphic_sprites[Globals.graphics_level]

		self.last_graphics = Globals.graphics_level 

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

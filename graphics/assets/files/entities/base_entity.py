# Default class for everything
from assets.files.utilities.globals import Globals
from assets.files.utilities.hitbox import Hitbox

import pygame
import time
import sys


class BaseEntity:

	# Gravity attributes
	is_grounded = None
	gravity_strength = None

	# Position  of the entity
	x = 0
	y = 0
	w = 0
	h = 0

	# The dimensions of the sprites
	img_w = 0
	img_h = 0

	# Whether or not the sprites change
	is_animated = False

	# The image if it is not animated
	graphic_images = []
	image = None

	# Animation sprites and indexes\
	graphic_sprites = []
	sprites = None
	sprite_indexes = None
	this_index = 0

	# The platform the entity is standing on
	platform_under = None

	# Graphics level
	last_graphics = Globals.graphics_level

	# Times for animation
	last_sprite_time = 0
	sprite_interval = 0

	facing_left = False

	last_time = 0
	last_position = None
	delta_time = 0

	is_showing = True

	# whether or not the entity is affected by gravity
	is_static = False

	# The entity's hitboxes
	hitboxes = None

	# Whether or not to play a death animation
	# Only used for enemies
	is_dying = False

	# The offset with which to draw the image
	image_offset_x = 0
	image_offset_y = 0

	# Initializes basic stats
	# Used by almost all entities
	def entity_init(self, x, y):

		# Scales the width/height relative
		self.h = self.scale_relative(self.h)
		self.w = self.scale_relative(self.w)

		# Sets the X/Y coords
		self.x = x * Globals.block_size
		self.y = y * Globals.block_size

		# Does basic initializing function
		self.resize_images()
		self.clip_to_hitboxes()

		if not self.is_animated:
			self.image = self.graphic_images[Globals.graphics_level]

		else:
			self.sprites = self.graphic_sprites[Globals.graphics_level]

	# Resizes all the images to the proper width/height
	def resize_images(self):

		# Resizes all sprites
		if self.is_animated:
			for x in range(len(self.graphic_sprites)):
				for i in range(len(self.graphic_sprites[x])):
					if self.is_static:
						self.graphic_sprites[x][i] = pygame.transform.scale(self.graphic_sprites[x][i], (self.w, self.h))
					else:
						self.graphic_sprites[x][i] = pygame.transform.scale(self.graphic_sprites[x][i], (self.w, self.h))

		# Resizes all images
		else:
			for i in range(len(self.graphic_images)):
				self.graphic_images[i] = pygame.transform.scale(self.graphic_images[i], (self.w, self.h))
			self.image = self.graphic_images[Globals.graphics_level]

	# Clips the entity dimensions to its hitboxes
	# helps with collision detection
	def clip_to_hitboxes(self):

		# Sets the default hitbox to be one block_size long
		if self.hitboxes is None:
			self.hitboxes = []
			self.add_hitbox(x=0, y=0, w=16, h=16)
			return

		# sets the image offsets to be very large
		self.image_offset_x = 5 * Globals.block_size
		self.image_offset_y = 5 * Globals.block_size

		# Cycles through to find the hitbox closest to the left/top

		for hb in self.hitboxes:
			if hb.offset_x < self.image_offset_x:
				self.image_offset_x = hb.offset_x

			if hb.offset_y < self.image_offset_y:
				self.image_offset_y = hb.offset_y

		# Changes all hitbox x/y values accordingly

		for hb in self.hitboxes:
			hb.offset_x -= self.image_offset_x
			hb.offset_y -= self.image_offset_y

		# Changes the player width/height to fit

		# Gets the most width/height
		most_w = 0
		most_h = 0
		for hb in self.hitboxes:

			if hb.offset_x + hb.w > most_w:
				most_w = hb.offset_x + hb.w

			if hb.offset_y + hb.h > most_h:
				most_h = hb.offset_y + hb.h

		# Sets the player's width/height
		self.w = most_w
		self.h = most_h

	def add_hitbox(self, x, y, w, h):

		if self.hitboxes is None:
			self.hitboxes = []

		x = self.scale_relative(x)
		y = self.scale_relative(y)
		w = self.scale_relative(w)
		h = self.scale_relative(h)

		self.hitboxes.append(Hitbox(x=x, y=y, w=w, h=h, parent=self))

	def set_delta_time(self):

		if self.last_time == 0:
			self.last_time = time.time()

		self.delta_time = (time.time() - self.last_time)

		self.last_time = time.time()

	@staticmethod
	def scale_relative(num):

		return int(num * (Globals.block_size / 16))

	def check_for_collision(self, target):

		for thb in target.hitboxes:

			for shb in self.hitboxes:
				
				if shb.y < thb.y + thb.h:
					if shb.y + shb.h > thb.y:
						if shb.x < thb.x + thb.w:
							if shb.x + shb.w > thb.x:
								return True
		return False

	def base_update(self):
		self.set_delta_time()

		if not Globals.is_paused:

			if not self.is_dying:

				if not self.is_static:
					self.gravity_update()

				self.update()

				for hb in self.hitboxes:
					hb.update()

				if not self.is_static:
					self.check_platform_collision()
			else:
				self.death_animation()

			self.check_if_fallen_out_of_level()

		if self.is_showing:
			self.render()

	def check_if_fallen_out_of_level(self):
		if self.y > Globals.level_height * Globals.block_size:
			self.death_animation()

	def print_hitboxes(self):
		for hb in self.hitboxes:
			print("x:%s, y:%s, w:%s, h:%s" % (hb.x, hb.y, hb.w, hb.h))

	def check_platform_collision(self):

		try:
			self.last_position['x']
			self.last_position['y']
		except TypeError:

			self.last_position = {
				"x": self.x,
				"y": self.y
			}

		for platform in Globals.platforms:

			if self.x + self.w > platform.x:
				if self.x < platform.x + platform.w:
					if self.y + self.h > platform.y:
						if self.y < platform.y + platform.h:

							if self.last_position['y'] > platform.y + platform.h and self.y < platform.y + platform.h:

								self.y = platform.y + platform.h

								self.momY *= -0.5

							if self.last_position['x'] >= platform.x + platform.w:
								if self.x < platform.x + platform.w:
									self.x = platform.x + platform.w

							elif self.last_position['x'] + self.w <= platform.x:
								if self.x + self.w > platform.x:
									self.x = platform.x - self.w

		self.last_position['x'] = self.x
		self.last_position['y'] = self.y

	def render(self):

		if self.is_animated:
			unix = time.time() * 1000

			if not Globals.is_paused:
				if self.last_sprite_time < unix - self.sprite_interval:

					self.this_index += 1
					self.last_sprite_time = time.time() * 1000

				if self.this_index >= len(self.sprite_indexes):
					self.this_index = 0

			try:

				sprite = self.sprites[self.sprite_indexes[self.this_index]]

			except IndexError:
				print("Sprite Index out of bounds.")
				print("---- Entity: %s" % self)
				print("---- Index: %s" % self.sprite_indexes[self.this_index])
				print("---- This Index: %s" % self.this_index)
				sys.exit(0)

		else:
			sprite = self.image

		x = self.x + Globals.camera_offset['x']
		y = self.y + Globals.camera_offset['y']

		if not self.is_static:

			# Moves the image over to fit with the hitboxes
			x -= self.image_offset_x
			y -= self.image_offset_y

		if not self.facing_left:

			sprite = pygame.transform.flip(sprite, True, False)

		Globals.window.blit(sprite, (x, y))

		if Globals.debug:

			red = (255, 0, 0)

			pygame.draw.rect(Globals.window, red, [self.x + Globals.camera_offset['x'], self.y + Globals.camera_offset['y'], self.w, self.h], 2)

			try:
				for hb in self.hitboxes:
					hb.debug_draw()
			except TypeError:
				pass

	def update_graphics(self):
				
		if not self.is_animated:

			self.image = self.graphic_images[Globals.graphics_level]
			
		else:

			self.sprites = self.graphic_sprites[Globals.graphics_level]

		self.last_graphics = Globals.graphics_level 

	def gravity_update(self):

		starting_y = self.y

		if self.is_grounded is False:

			self.momY -= Globals.gravity_strength * self.delta_time

			self.y -= self.momY * self.delta_time

			for platform in Globals.platforms:

				collide_x = False
				collide_y = False

				if self.x <= platform.x + platform.w:
					if self.x + self.w >= platform.x:

						collide_x = True

				if self.y + self.h >= platform.y:
					if starting_y + self.h <= platform.y:

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

			if platform is None or self.x > platform.x + platform.w or self.x + self.w < platform.x:

				self.is_grounded = False
				self.momY = 0
				self.platform_under = None

	def img_load(self, url):

		full_url = "assets/images/%s" % url
		image = pygame.image.load(full_url).convert_alpha()
		return image

	# Filler
	def death_animation(self):
		del self

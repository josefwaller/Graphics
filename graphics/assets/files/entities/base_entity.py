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

	img_w = 0
	img_h = 0

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

	last_position = {}

	is_showing = True
	is_static = False

	hitboxes = None

	least_x = 0
	least_y = 0


	def entity_init (self, x, y):

		if self.is_animated:

			self.img_h = self.make_pixelated(self.sprites[0].get_size()[1])
			self.img_w = self.make_pixelated(self.sprites[0].get_size()[0])

		else:
			self.h = self.make_pixelated(self.image.get_size()[1])
			self.w = self.make_pixelated(self.image.get_size()[0])

		self.x = x * Globals.block_size + (Globals.block_size - self.w) / 2
		self.y = y * Globals.block_size + (Globals.block_size - self.h) / 2

		self.least_x = 0
		self.least_y = 0

		self.resize_images()

		self.clip_to_hitboxes()
		
	def resize_images (self):

		if self.is_animated:

			for x in range(len(self.graphic_sprites)):

				for i in range(len(self.graphic_sprites[x])):

					if self.is_static:
						self.graphic_sprites[x][i] = pygame.transform.scale(self.graphic_sprites[x][i], (self.w, self.h))
					else:

						self.graphic_sprites[x][i] = pygame.transform.scale(self.graphic_sprites[x][i], (self.img_w, self.img_h))

		else:

			for i in range(len(self.graphic_images)):

				self.graphic_images[i] = pygame.transform.scale(self.graphic_images[i], (self.w, self.h))

			self.image = self.graphic_images[0]

	#Clips the entity dimensions to its hitboxes
	#helps with collision detection

	def clip_to_hitboxes (self):

		if self.hitboxes == None:

			self.hitboxes = []

			self.add_hitbox(x=0, y=0, w=16, h=16)
			return

		self.least_x = 5 * Globals.block_size
		self.least_y = 5 * Globals.block_size

		most_w = 0
		most_h = 0

		#Cycles through to find the hitbox closest to the left/top

		for hb in self.hitboxes:

			if hb.offset_x < self.least_x:

				self.least_x = hb.offset_x

			if hb.offset_y < self.least_y:

				self.least_y = hb.offset_y

		#Changes all hitbox x/y values accordingly

		for hb in self.hitboxes:

			hb.offset_x -= self.least_x

			hb.offset_y -= self.least_y

		#Changes the player width/height to fit

		for hb in self.hitboxes:

			if hb.offset_x + hb.w > most_w:

				most_w = hb.offset_x + hb.w

			if hb.offset_y + hb.h > most_h:

				most_h = hb.offset_y + hb.h

		self.w = most_w
		self.h = most_h


	def img_load(self, url):

		try:

			full_url = "assets/images/%s" % url 

			image = pygame.image.load(full_url).convert_alpha()

		except:
			pass

		return image 

	def add_hitbox (self, x, y, w, h):

		if self.hitboxes == None:
			self.hitboxes = []

		x = self.make_pixelated(x)
		y = self.make_pixelated(y)
		w = self.make_pixelated(w)
		h = self.make_pixelated(h)

		self.hitboxes.append(Hitbox(x=x, y=y, w=w, h=h, parent=self))

	def set_delta_time(self):

		if self.last_time == 0:
			self.last_time = time.time()

		self.delta_time = (time.time() - self.last_time)

		self.last_time = time.time()

	def make_pixelated(self, num):

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

		self.last_position['x'] = self.x
		self.last_position['y'] = self.y

		if not self.last_graphics == Globals.graphics_level:

			self.update_graphics()

		if not Globals.is_paused:

			if not self.is_static:
				self.gravity_update()
 
			self.update()

			# self.check_platform_collision()

			if self.is_showing:
				self.render()

			for hb in self.hitboxes:
				hb.update()

	def print_hitboxes (self):
		for hb in self.hitboxes:
			print("x:%s, y:%s, w:%s, h:%s" % (hb.x, hb.y, hb.w, hb.h))

	def check_platform_collision(self):

		for platform in Globals.platforms:

			if self.check_for_collision(platform):

				if self.last_position['x'] <= platform.x:

					self.x = platform.x - self.w

				else:
					self.x = platform.x + platform.w

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
		x = self.x + Globals.camera_offset['x']

		y = self.y + Globals.camera_offset['y']

		if not self.is_static:

			x -= self.least_x
			y -= self.least_y

		if not self.facing_left:

			sprite = pygame.transform.flip(sprite, True, False)

		Globals.window.blit(sprite, (x, y))

		if Globals.debug:

			red = (255, 0, 0)

			pygame.draw.rect(Globals.window, red, [self.x + Globals.camera_offset['x'], self.y, self.w, self.h], 2) 




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

				if self.x <= platform.x + platform.w:
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

			if platform == None or self.x > platform.x + platform.w or self.x + self.w < platform.x:

				self.is_grounded = False
				self.momY = 0
				self.platform_under = None

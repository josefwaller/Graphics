class Globals:
	block_size = None
	pixels_per_block = 0
	window = None
	camera_offset = {
		"x": 0,
		"y": 0
	}
	projectiles = []
	enemies = []
	tools = []
	current_tool = None
	player = None
	checkpoints = []
	platforms = []
	music = "16_game.wav"
	music_fade_out = None
	music_fade_in = True
	debug = False
	gravity_strength = 5
	graphics_level = 0
	is_paused = False
	hud = None
	props = []
	in_menu = True
	level_width = 0
	level_height = 0
	endblock = None
	volume = 1

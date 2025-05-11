import pygame
from sys import exit
from random import randint, choices

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame1.png').convert_alpha(),0.2)
		player_walk_2 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame2.png').convert_alpha(),0.2)
		player_walk_3 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame3.png').convert_alpha(),0.2)
		self.player_walk = [player_walk_1,player_walk_2,player_walk_3]
		self.player_index = 0
		self.player_jump = pygame.transform.scale_by(pygame.image.load('assets/player/player_jump_frame1.png').convert_alpha(),0.2)

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (200,535))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)
		self.velocity_x = 0 # horizontal velocity for fluxflip_horizontal*

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 535:
			self.gravity = -25
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 535:
			self.rect.bottom = 535

	def move_horizontal(self):
		self.rect.x += self.velocity_x
		self.velocity_x *= 0.9  # friction to slow down*

	def animation_state(self):
		if self.rect.bottom < 535:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.move_horizontal() #added*
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		self.type = type
		
		if type == 'coil_long':
			coil_long_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/coil_long_frame1.png').convert_alpha(),0.2)
			coil_long_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/coil_long_frame2.png').convert_alpha(),0.2)
			self.frames = [coil_long_1,coil_long_2]
			y_pos = 300
		if type == 'coil_short':
			coil_short_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/coil_short_frame1.png').convert_alpha(),0.2)
			coil_short_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/coil_short_frame2.png').convert_alpha(),0.2)
			self.frames = [coil_short_1,coil_short_2]
			y_pos = 300
		if type == 'openswitch':
			openswitch_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/openswitch_frame1.png').convert_alpha(),0.2)
			openswitch_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/openswitch_frame2.png').convert_alpha(),0.2)
			self.frames = [openswitch_1,openswitch_2]
			y_pos = 300
		if type == 'resistor':
			resistor_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/resistor_frame1.png').convert_alpha(),0.2)
			resistor_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/resistor_frame2.png').convert_alpha(),0.2)
			self.frames = [resistor_1,resistor_2]
			y_pos = 300
		if type == 'transformer_up':
			transformer_up_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_up_frame1.png').convert_alpha(),0.2)
			transformer_up_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_up_frame2.png').convert_alpha(),0.2)
			self.frames = [transformer_up_1,transformer_up_2]
			y_pos = 300
		if type == 'transformer_down':
			transformer_down_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_down_frame1.png').convert_alpha(),0.2)
			transformer_down_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_down_frame2.png').convert_alpha(),0.2)
			self.frames= [transformer_down_1,transformer_down_2]
			y_pos = 300
		if type == 'fluxflip_vertical':
			fluxflip_vertical_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_vertical_frame1.png').convert_alpha(),0.2)
			fluxflip_vertical_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_vertical_frame2.png').convert_alpha(),0.2)
			self.frames = [fluxflip_vertical_1,fluxflip_vertical_2]
			y_pos = 300
		if type == 'fluxflip_horizontal':
			fluxflip_horizontal_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_horizontal_frame1.png').convert_alpha(),0.2)
			fluxflip_horizontal_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_horizontal_frame2.png').convert_alpha(),0.2)
			self.frames = [fluxflip_horizontal_1,fluxflip_horizontal_2]
			y_pos = 300
		if type == 'roundabout':
			roundabout_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/roundabout_frame1.png').convert_alpha(),0.2)
			roundabout_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/roundabout_frame2.png').convert_alpha(),0.2)
			self.frames = [roundabout_1,roundabout_2]
			y_pos = 300
		if type == 'signswitcher':
			signswitcher_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/signswitcher_frame1.png').convert_alpha(),0.2)
			signswitcher_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/signswitcher_frame2.png').convert_alpha(),0.2)
			self.frames = [signswitcher_1,signswitcher_2]
			y_pos = 300
		if type == 'stick':
			stick_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame1.png').convert_alpha(),0.1)
			stick_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame2.png').convert_alpha(),0.1)
			self.frames = [stick_1,stick_2]
			y_pos = 300
		if type == 'portal':
			portal_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/portal.png').convert_alpha(),0.2)
			self.frames = [portal_1]
			y_pos = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	#score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	#score_rect = score_surf.get_rect(center = (400,50))
	#screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
    collided_obstacle = pygame.sprite.spritecollideany(player.sprite, obstacle_group)
    if collided_obstacle:
        return collided_obstacle
    return None


pygame.init()
screen = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Current Man')
clock = pygame.time.Clock()
#test_font = pygame.fme.time.Clockont.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
#additional sfx*
transformer_up_sound = pygame.mixer.Sound('audio/transformer_up.mp3')
transformer_up_sound.set_volume(1)
transformer_down_sound = pygame.mixer.Sound('audio/transformer_down.mp3')
transformer_down_sound.set_volume(1)
#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

zone_fire = 'fire'
zone_ice = 'ice'

fire_obstacles = ['coil_long','coil_short','openswitch','resistor','transformer_up','transformer_down','portal']
fire_weights = [2, 2, 2, 2, 2, 2, 1]
ice_obstacles = ['fluxflip_vertical','fluxflip_horizontal','roundabout','signswitcher','stick','portal']
ice_weights = [2, 2, 2, 2, 2, 1]

current_zone = zone_fire

fire_background = pygame.image.load('assets/environment/fire_bg.png').convert()
fire_floor = pygame.image.load('assets/environment/fire_floor.png').convert()
ice_background = pygame.image.load('assets/environment/ice_bg.png').convert()
ice_floor = pygame.image.load('assets/environment/ice_floor.png').convert()

screen_width, screen_height = screen.get_size()
fire_background_scaled = pygame.transform.scale(fire_background, (screen_width, screen_height))
ice_background_scaled = pygame.transform.scale(ice_background,(screen_width,screen_height))

# screenshake transformer_down*
def screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10):
# Select background and floor based on current zone
	background = fire_background_scaled if current_zone == zone_fire else ice_background_scaled
	floor = fire_floor if current_zone == zone_fire else ice_floor

	for _ in range(duration):
		offset_x = randint(-intensity, intensity)
		offset_y = randint(-intensity, intensity)

		# Draw background and floor with offset
		screen.blit(background, (offset_x, offset_y))
		screen.blit(floor, (0 + offset_x, 535 + offset_y))

		# Draw player and obstacles with offset
		for sprite in player:
			screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))
		for sprite in obstacle_group:
			screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))

		pygame.display.update()
		pygame.time.delay(20)

# Intro screen

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

last_obstacle_time = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				if current_zone == zone_fire:
					obstacle_type = choices(fire_obstacles, weights=fire_weights)[0]
				if current_zone == zone_ice:
					obstacle_type = choices(ice_obstacles, weights=ice_weights)[0]
				obstacle_group.add(Obstacle(obstacle_type))
				last_obstacle_time = pygame.time.get_ticks()

		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		if current_zone == zone_fire:
			screen.blit(fire_background_scaled,(0,0))
			screen.blit(fire_floor,(0,535))
		else:
			screen.blit(ice_background_scaled,(0,0))
			screen.blit(ice_floor,(0,535))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		collided_obstacle = collision_sprite()
		if collided_obstacle:
			if collided_obstacle.type in ['coil_long', 'coil_short']:
				print('coil')
				# put effect

			elif collided_obstacle.type == 'openswitch':
				print('openswitch')
				# put effect

			elif collided_obstacle.type == 'resistor':
				print('resistor')
				game_active = False
				# put effect

			elif collided_obstacle.type == 'transformer_up':
				print('transformer_up')
				player.sprite.gravity = -20  #accelerate upward*
				transformer_up_sound.play() # put effect*

			elif collided_obstacle.type == 'transformer_down':
				print('transformer_down')
				player.sprite.gravity += 15  # accelerate downward*
				transformer_down_sound.play()  # put effect*
				# Apply screenshake based on current zone*
				screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)

			elif collided_obstacle.type in ['fluxflip_horizontal', 'fluxflip_vertical']:
				print('fluxflip')
				if collided_obstacle.type == 'fluxflip_vertical':
					player.sprite.gravity = -20  # Launch upward like a jump*
					flux_sound = pygame.mixer.Sound('audio/fluxflip_vertical.wav')
					flux_sound.set_volume(10)
					flux_sound.play()
				elif collided_obstacle.type == 'fluxflip_horizontal':
					player.sprite.velocity_x = 15  # Push player rightward
					fluxflip_horizontal_sound = pygame.mixer.Sound('audio/fluxflip_horizontal.wav')
					fluxflip_horizontal_sound.set_volume(10)
					fluxflip_horizontal_sound.play()
			# put effect

			elif collided_obstacle.type == 'roundabout':
				print('roundabout')
				# put effect

			elif collided_obstacle.type == 'signswitcher':
				print('signswitcher')
				# put effect

			elif collided_obstacle.type == 'stick':
				print('stick')
				# put effect

			elif collided_obstacle.type == 'portal':
				if current_zone == zone_fire:
					current_zone = zone_ice
				else:
					current_zone = zone_fire
				obstacle_group.empty()

			collided_obstacle.kill()

		else:
			game_active = True


	else:
		screen.fill((94,129,162))
		

		#score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		#score_message_rect = score_message.get_rect(center = (400,330))
		#screen.blit(game_name,game_name_rect)

		#if score == 0: screen.blit(game_message,game_message_rect)
		#else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
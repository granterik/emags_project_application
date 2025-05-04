import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (200,535))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

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
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fluxflip_vertical':
			fluxflip_vertical_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_vertical_frame1.png').convert_alpha(),0.2)
			fluxflip_vertical_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_vertical_frame2.png').convert_alpha(),0.2)
			self.frames = [fluxflip_vertical_1,fluxflip_vertical_2]
			y_pos = 210
		if type == 'fluxflip_horizontal':
			fluxflip_horizontal_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_horizontal_frame1.png').convert_alpha(),0.2)
			fluxflip_horizontal_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_horizontal_frame2.png').convert_alpha(),0.2)
			self.frames = [fluxflip_horizontal_1,fluxflip_horizontal_2]
			y_pos = 300
		if type == 'roundabout':
			roundabout_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/roundabout_frame1.png').convert_alpha(),0.2)
			roundabout_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/roundabout_frame2.png').convert_alpha(),0.2)
			self.frames = [roundabout_1,roundabout_2]
			y_pos = 100
		if type == 'signswitcher':
			signswitcher_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/signswitcher_frame1.png').convert_alpha(),0.2)
			signswitcher_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/signswitcher_frame2.png').convert_alpha(),0.2)
			self.frames = [signswitcher_1,signswitcher_2]
			y_pos = 350
		else:
			stick_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame1.png').convert_alpha(),0.2)
			stick_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame2.png').convert_alpha(),0.2)
			self.frames = [stick_1,stick_2]
			y_pos = 500

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
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((1000,700))
pygame.display.set_caption('Current Man')
clock = pygame.time.Clock()
#test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

hell_background = pygame.image.load('assets/environment/hell_bg_temp.png').convert()
hell_floor = pygame.image.load('assets/environment/hell_floor.png').convert()
ocean_background = pygame.image.load('assets/environment/ocean_bg_temp.png').convert()
ocean_floor = pygame.image.load('assets/environment/ocean_floor.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

#game_name = test_font.render('Pixel Runner',False,(111,196,169))
#game_name_rect = game_name.get_rect(center = (400,80))

#game_message = test_font.render('Press space to run',False,(111,196,169))
#game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fluxflip_vertical','fluxflip_horizontal','roundabout','signswitcher','stick'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(ocean_background,(0,0))
		screen.blit(ocean_floor,(0,535))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		#score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		#score_message_rect = score_message.get_rect(center = (400,330))
		#screen.blit(game_name,game_name_rect)

		#if score == 0: screen.blit(game_message,game_message_rect)
		#else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
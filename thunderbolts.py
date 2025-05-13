import pygame
from sys import exit
from random import randint, choices
import math




class Player(pygame.sprite.Sprite):
   def __init__(self):
       super().__init__()
       player_walk_1 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame1.png').convert_alpha(),
                                                 0.2)
       player_walk_2 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame2.png').convert_alpha(),
                                                 0.2)
       player_walk_3 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame3.png').convert_alpha(),
                                                 0.2)
       self.player_walk = [player_walk_1, player_walk_2, player_walk_3]
       self.player_index = 0
       self.player_jump = pygame.transform.scale_by(
           pygame.image.load('assets/player/player_jump_frame1.png').convert_alpha(), 0.2)


       self.image = self.player_walk[self.player_index]
       self.rect = self.image.get_rect(midbottom=(200, 535))
       self.gravity = 0
       self.speed = 5


       self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
       self.jump_sound.set_volume(0.5)
       self.velocity_x = 0  # horizontal velocity for fluxflip_horizontal*


       self.sign = 1
       self.switch_sound = pygame.mixer.Sound('audio/signswitcher.mp3')
       self.switch_sound.set_volume(0.9)


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
           if self.player_index >= len(self.player_walk): self.player_index = 0
           self.image = self.player_walk[int(self.player_index)]


   def switch_sign(self):
       self.sign *= -1
       self.switch_sound.play()
       print(f'Sign altered. New sign: {self.sign}')


   def roundabout_collision(self, obstacle_group):
       for obj in obstacle_group.sprites():
           if getattr(obj, 'type', None) == 'roundabout':
               dx = self.rect.centerx - obj.rect.centerx
               dy = self.rect.centery - obj.rect.centery
               distance = math.hypot(dx, dy) or 1


               if distance < 200:  # ⬅️ Increase effect radius (from default ~100 to 200)
                   # Normalize direction
                   dx /= distance
                   dy /= distance


                   force_magnitude = max(0, 250 - distance) / 2  # ⬅️ Stronger force as you get closer


                   if self.sign == 1:
                       # Positive: Repelled
                       self.rect.x += int(dx * force_magnitude)
                       self.rect.y += int(dy * force_magnitude)
                   else:
                       # Negative: Attracted
                       self.rect.x -= int(dx * force_magnitude)
                       self.rect.y -= int(dy * force_magnitude)
                       screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)


                       if distance < 40:
                           self.rect.center = obj.rect.center


   def update(self):
       self.player_input()
       self.apply_gravity()
       self.move_horizontal()  # added*
       self.animation_state()
       SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
       keys = pygame.key.get_pressed()


       if keys[pygame.K_LEFT]:
           self.rect.x -= self.speed
       if keys[pygame.K_RIGHT]:
           self.rect.x += self.speed
       if self.rect.left < 0:
           self.rect.left = 0
       if keys[pygame.K_UP]:
           self.rect.y -= self.speed
       if keys[pygame.K_DOWN]:
           self.rect.y += self.speed
       if self.rect.right > SCREEN_WIDTH:
           self.rect.right = SCREEN_WIDTH
       if self.rect.top < 0:
           self.rect.top = 0
       if self.rect.bottom > SCREEN_HEIGHT:
           self.rect.bottom = SCREEN_HEIGHT




class Obstacle(pygame.sprite.Sprite):
   def __init__(self, type):
       super().__init__()
       self.type = type


       if type == 'coil_short':
           coil_short_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/coil_short_frame1.png').convert_alpha(), 0.1)
           coil_short_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/coil_short_frame2.png').convert_alpha(), 0.1)
           self.frames = [coil_short_1, coil_short_2]
           y_pos = 640
       if type == 'openswitch':
           openswitch_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/openswitch_frame1.png').convert_alpha(), 0.4)
           openswitch_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/openswitch_frame2.png').convert_alpha(), 0.4)
           self.frames = [openswitch_1, openswitch_2]
           y_pos = 540
       if type == 'resistor':
           resistor_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/resistor_frame1.png').convert_alpha(), 0.2)
           resistor_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/resistor_frame2.png').convert_alpha(), 0.2)
           self.frames = [resistor_1, resistor_2]
           y_pos = 300
       if type == 'transformer_up':
           transformer_up_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/transformer_up_frame1.png').convert_alpha(), 0.2)
           transformer_up_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/transformer_up_frame2.png').convert_alpha(), 0.2)
           self.frames = [transformer_up_1, transformer_up_2]
           y_pos = 300
       if type == 'transformer_down':
           transformer_down_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/transformer_down_frame1.png').convert_alpha(), 0.2)
           transformer_down_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/transformer_down_frame2.png').convert_alpha(), 0.2)
           self.frames = [transformer_down_1, transformer_down_2]
           y_pos = 300
       if type == 'fluxflip_vertical':
           fluxflip_vertical_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/fluxflip_vertical_frame1.png').convert_alpha(), 0.2)
           fluxflip_vertical_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/fluxflip_vertical_frame2.png').convert_alpha(), 0.2)
           self.frames = [fluxflip_vertical_1, fluxflip_vertical_2]
           y_pos = 300
       if type == 'fluxflip_horizontal':
           fluxflip_horizontal_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/fluxflip_horizontal_frame1.png').convert_alpha(), 0.2)
           fluxflip_horizontal_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/fluxflip_horizontal_frame2.png').convert_alpha(), 0.2)
           self.frames = [fluxflip_horizontal_1, fluxflip_horizontal_2]
           y_pos = 300
       if type == 'roundabout':
           roundabout_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/roundabout_frame1.png').convert_alpha(), 0.2)
           roundabout_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/roundabout_frame2.png').convert_alpha(), 0.2)
           self.frames = [roundabout_1, roundabout_2]
           y_pos = 300
       if type == 'signswitcher':
           signswitcher_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/signswitcher_frame1.png').convert_alpha(), 0.2)
           signswitcher_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/signswitcher_frame2.png').convert_alpha(), 0.2)
           self.frames = [signswitcher_1, signswitcher_2]
           y_pos = 300
       if type == 'stick':
           stick_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame1.png').convert_alpha(),
                                               0.12)
           stick_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame2.png').convert_alpha(),
                                               0.12)
           self.original_frames = [stick_1, stick_2]
           self.frames = self.original_frames.copy()
           self.stick_angle = 0
           y_pos = 300
       if type == 'portal':
           portal_1 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/portal_frame1.png').convert_alpha(), 0.2)
           portal_2 = pygame.transform.scale_by(
               pygame.image.load('assets/obstacles/portal_frame2.png').convert_alpha(), 0.2)
           self.frames = [portal_1, portal_2]
           y_pos = 300


       self.animation_index = 0
       self.image = self.frames[self.animation_index]
       self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))


   def animation_state(self):
       self.animation_index += 0.1
       if self.animation_index >= len(self.frames): self.animation_index = 0
       self.image = self.frames[int(self.animation_index)]


   def switch_sign(self):
       self.sign *= -1
       self.switch_sound.play()
       print(f'Sign altered. New sign: {self.sign}')


   def update(self):
       self.animation_state()
       if self.type == 'stick':
           self.stick_angle += 6
           self.frames = [pygame.transform.rotate(img, self.stick_angle) for img in self.original_frames]
           self.image = self.frames[int(self.animation_index)]


           # Move left like other obstacles
           self.rect.x -= 6


           # Keep rotation center aligned as it moves
           self.rect = self.image.get_rect(center=self.rect.center)
       else:
           self.rect.x -= 6


       self.destroy()


   def destroy(self):
       if self.rect.x <= -100:
           self.kill()




def display_score():
   current_time = int(pygame.time.get_ticks() / 1000) - start_time
   # score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
   # score_rect = score_surf.get_rect(center = (400,50))
   # screen.blit(score_surf,score_rect)
   return current_time




def collision_sprite():
   collided_obstacle = pygame.sprite.spritecollideany(player.sprite, obstacle_group)
   if collided_obstacle:
       return collided_obstacle
   return None




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




pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Current Man')
clock = pygame.time.Clock()  # test_font = pygame.fme.time.Clockont.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)
transformer_up_sound = pygame.mixer.Sound('audio/transformer_up.mp3')
transformer_up_sound.set_volume(1)
transformer_down_sound = pygame.mixer.Sound('audio/transformer_down.mp3')
transformer_down_sound.set_volume(1)
player = pygame.sprite.GroupSingle()
player.add(Player())


obstacle_group = pygame.sprite.Group()


zone_fire = 'fire'
zone_ice = 'ice'


fire_obstacles = ['coil_short', 'openswitch', 'resistor', 'transformer_up', 'transformer_down', 'portal']
fire_weights = [2, 2, 2, 2, 2, 1]
ice_obstacles = ['fluxflip_vertical', 'fluxflip_horizontal', 'roundabout', 'signswitcher', 'stick', 'portal']
ice_weights = [2, 2, 2, 2, 2, 1]


current_zone = zone_fire


fire_background = pygame.image.load('assets/environment/fire_bg.png').convert()
fire_floor = pygame.image.load('assets/environment/fire_floor.png').convert()
ice_background = pygame.image.load('assets/environment/ice_bg.png').convert()
ice_floor = pygame.image.load('assets/environment/ice_floor.png').convert()


screen_width, screen_height = screen.get_size()
fire_background_scaled = pygame.transform.scale(fire_background, (screen_width, screen_height))
ice_background_scaled = pygame.transform.scale(ice_background, (screen_width, screen_height))


# Intro screen




# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


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
           screen.blit(fire_background_scaled, (0, 0))
           screen.blit(fire_floor, (0, 535))
       else:
           screen.blit(ice_background_scaled, (0, 0))
           screen.blit(ice_floor, (0, 535))
       score = display_score()


       player.draw(screen)
       player.update()
       player.sprite.roundabout_collision(obstacle_group)


       obstacle_group.draw(screen)
       obstacle_group.update()


       collided_obstacle = collision_sprite()
       if collided_obstacle:
           if collided_obstacle.type in ['coil_short']:
               slow_start_time = pygame.time.get_ticks()
               obstacle_group.slow_effect_active = True
               obstacle_group.slow_effect_timer = slow_start_time


               original_update = Obstacle.update




               def slowed_update(self):
                   speed = 2 if getattr(obstacle_group, 'slow_effect_active',
                                        False) and pygame.time.get_ticks() - obstacle_group.slow_effect_timer < 2000 else 6
                   self.animation_state()
                   self.rect.x -= speed


                   if pygame.time.get_ticks() - obstacle_group.slow_effect_timer >= 2000:
                       obstacle_group.slow_effect_active = False
                       Obstacle.update = original_update  # restore normal speed




               Obstacle.update = slowed_update




           elif collided_obstacle.type == 'openswitch':
               player.sprite.gravity = 22  # still affects the player


               # Bright fog-like overlay (light yellowish fog)
               fog_surface = pygame.Surface((screen_width, screen_height))
               fog_surface.fill((255, 255, 210))
               fog_surface.set_alpha(180)




               def draw_foggy_lightning(surface, start, depth, thickness):
                   if depth <= 0:
                       return
                   segment_len = randint(40, 60)
                   offset = (randint(-50, 50), segment_len)
                   end = (start[0] + offset[0], start[1] + offset[1])


                   # White-hot lightning core
                   pygame.draw.line(surface, (255, 255, 255), start, end, thickness + 2)
                   # Yellow outer glow
                   pygame.draw.line(surface, (255, 255, 120), start, end, thickness)


                   draw_foggy_lightning(surface, end, depth - 1, thickness)




               for i in range(6):
                   # Slightly heavier shake
                   offset = (randint(-12, 12), randint(-10, 10))
                   screen.blit(fog_surface, offset)


                   # Multiple large, fog-cutting bolts
                   for _ in range(4):
                       start_x = randint(200, 800)
                       draw_foggy_lightning(screen, (start_x, 0), depth=5, thickness=4)


                   pygame.display.update()
                   pygame.time.delay(40)
                   screen.fill((40, 40, 40))  # Slight smoky black background


               pygame.time.set_timer(pygame.USEREVENT + 2, 1000, loops=1)




           elif collided_obstacle.type == 'resistor':
               game_active = False




           elif collided_obstacle.type == 'transformer_up':
               player.sprite.gravity = -20  # accelerate upward*
               transformer_up_sound.play()  # put effect*




           elif collided_obstacle.type == 'transformer_down':
               player.sprite.gravity += 15  # accelerate downward*
               transformer_down_sound.play()  # put effect*
               # Apply screenshake based on current zone*
               screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)




           elif collided_obstacle.type in ['fluxflip_horizontal', 'fluxflip_vertical']:
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
               player.sprite.roundabout_collision(obstacle_group)




           elif collided_obstacle.type == 'signswitcher':
               print('signswitcher')
               player.sprite.switch_sign()




           elif collided_obstacle.type == 'stick':
               player.sprite.stuck_timer = 90


               for i in range(6):
                   # Freezing overlay building up
                   freeze_surface = pygame.Surface((screen_width, screen_height))
                   freeze_surface.fill((180, 230, 255))
                   freeze_surface.set_alpha(40 + i * 15)
                   screen.blit(freeze_surface, (0, 0))


                   # Horizontal shock arcs — lower part of screen (ground-level)
                   for _ in range(6):
                       start_x = randint(100, 900)
                       start_y = randint(550, 640)  # Lowered
                       end_x = start_x + randint(-100, 100)
                       end_y = start_y + randint(-40, 40)
                       pygame.draw.line(screen, (180, 255, 255), (start_x, start_y), (end_x, end_y), 3)




                   # Vertical bolts from sky — THICK & POWERFUL like in openswitch
                   def draw_downward_lightning(surface, start, depth, thickness):
                       if depth <= 0:
                           return
                       seg_len = randint(40, 60)
                       end = (start[0] + randint(-40, 40), start[1] + seg_len)
                       # Core and glow
                       pygame.draw.line(surface, (255, 255, 255), start, end, thickness + 1)
                       pygame.draw.line(surface, (255, 255, 100), start, end, thickness)
                       draw_downward_lightning(surface, end, depth - 1, thickness)




                   if i >= 1:
                       for _ in range(2):
                           x = randint(100, 300)
                           draw_downward_lightning(screen, (x, 0), 5, 4)


                   if i >= 2:
                       for _ in range(2):
                           x = randint(400, 600)
                           draw_downward_lightning(screen, (x, 0), 5, 4)


                   if i >= 3:
                       for _ in range(2):
                           x = randint(700, 900)
                           draw_downward_lightning(screen, (x, 0), 5, 4)


                   # Final shimmer burst
                   if i == 5:
                       for _ in range(4):
                           x = randint(300, 700)
                           y = randint(500, 600)
                           pygame.draw.line(screen, (255, 255, 255), (x, y),
                                            (x + randint(-60, 60), y + randint(-40, 40)), 2)


                       # SMOKE blast
                       smoke = pygame.Surface((screen_width, screen_height))
                       smoke.fill((120, 120, 120))
                       smoke.set_alpha(120)
                       screen.blit(smoke, (0, 0))


                   pygame.display.update()
                   pygame.time.delay(90)


               pygame.time.delay(350)








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
       screen.fill((94, 129, 162))


       # score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
       # score_message_rect = score_message.get_rect(center = (400,330))
       # screen.blit(game_name,game_name_rect)


       # if score == 0: screen.blit(game_message,game_message_rect)
       # else: screen.blit(score_message,score_message_rect)


   pygame.display.update()
   clock.tick(60)










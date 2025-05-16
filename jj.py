import pygame
pygame.init()
import sys
import random
from sys import exit
from random import randint, choices
import math

main_menu_music = pygame.mixer.Sound('audio/main_menu_lumiere.mp3')
game_over_music = pygame.mixer.Sound('audio/game_over_ghastly.mp3')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame1.png').convert_alpha(),0.2)
        player_walk_2 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame2.png').convert_alpha(),0.2)
        player_walk_3 = pygame.transform.scale_by(pygame.image.load('assets/player/player_frame3.png').convert_alpha(),0.2)
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3]
        self.player_index = 0
        self.player_jump = pygame.transform.scale_by(pygame.image.load('assets/player/player_jump_frame1.png').convert_alpha(), 0.2)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 535))
        self.gravity = 0
        self.speed = 5

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        self.velocity_x = 0  # horizontal velocity for fluxflip_horizontal*
        self.velocity_y = 0
        self.dead = False
        self.screenshake_done = False
        self.death_timer = 0

        self.sign = 1
        self.switch_sound = pygame.mixer.Sound('audio/signswitcher.mp3')
        self.switch_sound.set_volume(0.9)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 535:
            self.gravity = -28
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
        self.sign *= - 1
        self.switch_sound.play()

    def roundabout_collision(self, obstacle_group):
        for obj in obstacle_group.sprites():
            if getattr(obj, 'type', None) == 'roundabout':
                dx = self.rect.centerx - obj.rect.centerx
                dy = self.rect.centery - obj.rect.centery
                distance = math.hypot(dx, dy) or 1

                if distance < 200:
                    dx /= distance
                    dy /= distance
                    force_magnitude = max(0, 250 - distance) / 2

                    if self.sign == 1:
                        self.rect.x += int(dx * force_magnitude)
                        self.rect.y += int(dy * force_magnitude)
                    else:
                        self.rect.x -= int(dx * force_magnitude)
                        self.rect.y -= int(dy * force_magnitude)

                        if distance < 20:
                            self.rect.center = obj.rect.center

                        attraction(screen, center=(player.sprite.rect.centerx, player.sprite.rect.centery))

                        if not self.dead:
                            screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)
                            self.dead = True
                            self.death_timer = pygame.time.get_ticks()

                        elif self.dead and not self.screenshake_done:
                            if pygame.time.get_ticks() - self.death_timer >= 900:
                                self.screenshake_done = True
                                show_gameover_screen(screen, gameover_screen)

    def stick_collision(self, obstacle_group):
        for obj in obstacle_group:
            obstacle_center = obj.rect.center
            dx = self.rect.centerx - obstacle_center[0]
            dy = self.rect.centery - obstacle_center[1]
            distance = math.hypot(dx, dy) or 1
            if getattr(obj, 'type', None) == 'stick' and distance < 200:
                stick_angle = math.radians(obj.stick_angle)
                stick_dir_x = math.cos(stick_angle)
                stick_dir_y = math.sin(stick_angle)
                dot = dx * stick_dir_x + dy * stick_dir_y
                dx /= distance
                dy /= distance
                force_magnitude = max(0, 250 - distance) / 2
                if dot > 0:
                    stick_polarity = - 1
                else:
                    stick_polarity = 1

                if self.sign == stick_polarity:
                    self.rect.x += int(dx * force_magnitude)
                    self.rect.y += int(dy * force_magnitude)
                    # repulsion(screen, center=(player.sprite.rect.centerx, player.sprite.rect.centery))
                else:
                    self.rect.x -= int(dx * force_magnitude)
                    self.rect.y -= int(dy * force_magnitude)
                    if distance < 20:
                        self.rect.center = obj.rect.center
                    attraction(screen, center=(player.sprite.rect.centerx, player.sprite.rect.centery))

                    if not self.dead:
                        screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)
                        self.dead = True
                        self.death_timer = pygame.time.get_ticks()
                    elif self.dead and not self.screenshake_done:
                        if pygame.time.get_ticks() - self.death_timer >= 600:
                            self.screenshake_done = True
                            show_gameover_screen(screen, gameover_screen)

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

        self.roundabout_collision(obstacle_group)
        self.stick_collision(obstacle_group)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.velocity_y = 0

        if type == 'coil_short':
            coil_short_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/coil_short_frame1.png').convert_alpha(), 0.28)
            coil_short_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/coil_short_frame2.png').convert_alpha(), 0.28)
            self.frames = [coil_short_1, coil_short_2]
            y_pos = 535
        if type == 'openswitch':
            openswitch_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/openswitch_frame1.png').convert_alpha(), 0.25)
            openswitch_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/openswitch_frame2.png').convert_alpha(), 0.25)
            self.frames = [openswitch_1, openswitch_2]
            y_pos = 535
        if type == 'resistor':
            resistor_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/resistor_frame1.png').convert_alpha(), 0.2)
            resistor_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/resistor_frame2.png').convert_alpha(), 0.2)
            self.frames = [resistor_1, resistor_2]
            y_pos = random.choice([200, 300])
        if type == 'transformer_up':
            transformer_up_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_up_frame1.png').convert_alpha(), 0.2)
            transformer_up_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_up_frame2.png').convert_alpha(), 0.2)
            self.frames = [transformer_up_1, transformer_up_2]
            y_pos = random.choice([300, 535])
        if type == 'transformer_down':
            transformer_down_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_down_frame1.png').convert_alpha(), 0.2)
            transformer_down_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/transformer_down_frame2.png').convert_alpha(), 0.2)
            self.frames = [transformer_down_1, transformer_down_2]
            y_pos = random.choice([200, 300])
        if type == 'fluxflip_vertical':
            fluxflip_vertical_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_vertical_frame1.png').convert_alpha(), 0.2)
            fluxflip_vertical_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_vertical_frame2.png').convert_alpha(), 0.2)
            self.frames = [fluxflip_vertical_1, fluxflip_vertical_2]
            y_pos = random.choice([300, 535])
        if type == 'fluxflip_horizontal':
            fluxflip_horizontal_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_horizontal_frame1.png').convert_alpha(), 0.2)
            fluxflip_horizontal_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/fluxflip_horizontal_frame2.png').convert_alpha(), 0.2)
            self.frames = [fluxflip_horizontal_1, fluxflip_horizontal_2]
            y_pos = random.choice([200, 300, 535])
        if type == 'roundabout':
            roundabout_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/roundabout_frame1.png').convert_alpha(), 0.18)
            roundabout_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/roundabout_frame2.png').convert_alpha(), 0.18)
            self.frames = [roundabout_1, roundabout_2]
            y_pos = random.choice([300, 535])
        if type == 'signswitcher':
            signswitcher_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/signswitcher_frame1.png').convert_alpha(), 0.2)
            signswitcher_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/signswitcher_frame2.png').convert_alpha(), 0.2)
            self.frames = [signswitcher_1, signswitcher_2]
            y_pos = random.choice([200, 300, 535])
        if type == 'stick':
            stick_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame1.png').convert_alpha(),0.12)
            stick_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/stick_frame2.png').convert_alpha(),0.12)
            self.original_frames = [stick_1, stick_2]
            self.frames = self.original_frames.copy()
            self.stick_angle = 0
            y_pos = 250
        if type == 'portal':
            portal_1 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/portal_frame1.png').convert_alpha(), 0.2)
            portal_2 = pygame.transform.scale_by(pygame.image.load('assets/obstacles/portal_frame2.png').convert_alpha(), 0.2)
            self.frames = [portal_1, portal_2]
            y_pos = random.choice([200, 300, 535])

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

    def update(self):
        self.animation_state()
        if self.type == 'stick':
            self.stick_angle += 6
            self.frames = [pygame.transform.rotate(img, self.stick_angle) for img in self.original_frames]
            self.image = self.frames[int(self.animation_index)]

            # Move left like other obstacles
            self.rect.x -= 4

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
    background = fire_background_scaled if current_zone == zone_fire else ice_background_scaled
    floor = fire_floor if current_zone == zone_fire else ice_floor

    for _ in range(duration):
        offset_x = randint(-intensity, intensity)
        offset_y = randint(-intensity, intensity)

        screen.blit(background, (offset_x, offset_y))
        screen.blit(floor, (0 + offset_x, 535 + offset_y))

        for sprite in player:
            screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))
        for sprite in obstacle_group:
            screen.blit(sprite.image, sprite.rect.move(offset_x, offset_y))

        pygame.display.update()
        pygame.time.delay(20)
        screenshake_status = True

def show_gameover_screen(screen, gameover_screen):
    global game_active
    fight_ost_music.stop()
    game_over_music.play(loops=-1)

    screen.blit(gameover_screen, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                game_over_music.stop()
                main_menu_music.play(loops=-1)
                waiting = False

    game_active = False
    reset_game_state()

def death_animation(player, screen, clock):
    global is_in_death_animation

    if not is_in_death_animation:
        is_in_death_animation = True

        original_sprite = player.sprite
        original_rect = original_sprite.rect.copy()
        original_y = original_sprite.rect.y

        screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.time.delay(50)

        frozen_background = screen.copy()

        lift_height = 30
        lifted_y = max(0, original_y - lift_height)
        original_sprite.rect.y = lifted_y

        screen.blit(frozen_background, (0, 0))
        screen.blit(original_sprite.image, original_sprite.rect)
        pygame.display.flip()

        pygame.time.wait(900)

        fall_speed = 5
        while original_sprite.rect.y < screen.get_height():
            original_sprite.rect.y += fall_speed
            screen.blit(frozen_background, (0, 0))
            screen.blit(original_sprite.image, original_sprite.rect)
            pygame.display.flip()
            clock.tick(60)

        original_sprite.rect = original_rect

        is_in_death_animation = False

def quick_light_flashes(screen, flash_color=(180, 60, 60), flash_count=2, flash_duration=80, background_color=(40, 40, 40)):
    for _ in range(flash_count):
        screen.fill(flash_color)
        pygame.display.update()
        pygame.time.delay(flash_duration)

        screen.fill(background_color)
        pygame.display.update()
        pygame.time.delay(flash_duration)

def start_haze(haze_color=(180, 60, 60), haze_duration=10000000, alpha=100):
    return {
        "active": True,
        "start_time": pygame.time.get_ticks(),
        "duration": haze_duration,
        "surface": create_haze_surface(haze_color, alpha)
    }

def create_haze_surface(haze_color, alpha):
    haze_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    haze_surface.fill(haze_color)
    haze_surface.set_alpha(alpha)
    return haze_surface

def draw_haze(screen, haze_data):
    if haze_data["active"]:
        current_time = pygame.time.get_ticks()
        if current_time - haze_data["start_time"] < haze_data["duration"]:
            screen.blit(haze_data["surface"], (0, 0))
        else:
            haze_data["active"] = False

def repulsion(screen, center, burst_count=5, max_radius=60, color=(255, 60, 60), thickness=2):
    for i in range(burst_count):
        radius = int((i + 1) * max_radius / burst_count)
        alpha = max(0, 255 - i * 40)  # Fade out over distance

        # Create a transparent surface for the burst
        burst_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        pygame.draw.circle(burst_surface, (*color, alpha), center, radius, thickness)
        screen.blit(burst_surface, (0, 0))

        pygame.display.update()
        pygame.time.delay(30)  # Adjust for speed of repulsion

def attraction(screen, center, arrow_count=8, length=40, color=(120, 255, 120), speed=5):
    arrow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for frame in range(length // speed):
        arrow_surface.fill((0, 0, 0, 0))  # Clear the surface

        for i in range(arrow_count):
            angle = (2 * math.pi / arrow_count) * i
            dist = length - frame * speed
            x = int(center[0] + math.cos(angle) * dist)
            y = int(center[1] + math.sin(angle) * dist)

            end = (center[0], center[1])
            pygame.draw.line(arrow_surface, color, (x, y), end, 2)

            # Optional arrowhead
            head_size = 6
            dx = center[0] - x
            dy = center[1] - y
            angle_to_center = math.atan2(dy, dx)
            left = (x + math.cos(angle_to_center + 0.5) * head_size,
                    y + math.sin(angle_to_center + 0.5) * head_size)
            right = (x + math.cos(angle_to_center - 0.5) * head_size,
                     y + math.sin(angle_to_center - 0.5) * head_size)
            pygame.draw.polygon(arrow_surface, color, [left, right, end])

        screen.blit(arrow_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

def reset_game_state():
    global current_zone

    # Reset zone to fire
    current_zone = 'fire'

    # Reset player state
    player.sprite.rect.midbottom = (200, 535)
    player.sprite.sign = -1
    player.sprite.gravity = 0
    player.sprite.dead = False
    player.sprite.screenshake_done = False

    # Reset obstacle group
    obstacle_group.empty()

    # Reset time
    return pygame.time.get_ticks()

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Joule Jump')
clock = pygame.time.Clock()
# test_font = pygame.fme.time.Clockont.Font('font/Pixeltype.ttf', 50)
game_active = False
screenshake_status = False
attraction_status = False
is_in_death_animation = False
instruction_step = 0
credits_screen = 0
start_time = 0
score = 0
main_menu_music.play(loops=-1)
transformer_up_sound = pygame.mixer.Sound('audio/transformer_up.mp3')
transformer_up_sound.set_volume(1)
transformer_down_sound = pygame.mixer.Sound('audio/transformer_down.mp3')
transformer_down_sound.set_volume(1)
jj_title = pygame.image.load('assets/environment/title_screen.png').convert()
gameover_screen = pygame.image.load('assets/environment/game_over.png').convert()


player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

player.sprite.sign *= -1
sign1_img = pygame.image.load('assets/obstacles/possign.png').convert_alpha()
sign2_img = pygame.image.load('assets/obstacles/negsign.png').convert_alpha()
sign1_img = pygame.transform.scale(sign1_img, (400, 200))
sign2_img = pygame.transform.scale(sign2_img, (400, 200))

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

instructions_1 = pygame.image.load('assets/environment/instructions_page1.png').convert()
instructions_2 = pygame.image.load('assets/environment/instructions_page2.png').convert()
instructions_3 = pygame.image.load('assets/environment/instructions_page3.png').convert()
instructions_4 = pygame.image.load('assets/environment/instructions_page4.png').convert()
instructions_5 = pygame.image.load('assets/environment/instructions_page5.png').convert()
credits_1 = pygame.image.load('assets/environment/credits.png').convert()

screen_width, screen_height = screen.get_size()
fire_background_scaled = pygame.transform.scale(fire_background, (screen_width, screen_height))
ice_background_scaled = pygame.transform.scale(ice_background, (screen_width, screen_height))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_menu_music.stop()
                game_active = True
                fight_ost_music = random.choice([pygame.mixer.Sound('audio/fight_ost1_gestralsummerparty.mp3'), pygame.mixer.Sound('audio/fight_ost2_inlumieresname.mp3'),
                                                 pygame.mixer.Sound('audio/fight_ost3_megabot33.mp3'), pygame.mixer.Sound('audio/fight_ost4_volcanomines.mp3')])
                fight_ost_music.play(loops=-1)
                start_time = int(pygame.time.get_ticks() / 1000)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                instruction_step = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and instruction_step > 0:
                instruction_step = min(instruction_step + 1, 5)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and instruction_step > 1:
                instruction_step -= 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c and credits_screen == 0:
                credits_screen = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                instruction_step = 0
                credits_screen = 0

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
        player.sprite.stick_collision(obstacle_group)

        if not is_in_death_animation:
            player.draw(screen)
        sign_pic = sign1_img if player.sprite.sign == 1 else sign2_img
        sign_rect = sign_pic.get_rect(midleft=(player.sprite.rect.left - 280, player.sprite.rect.centery - 20))
        screen.blit(sign_pic, sign_rect)
        obstacle_group.draw(screen)
        obstacle_group.update()

        collided_obstacle = collision_sprite()
        if collided_obstacle:
            if collided_obstacle.type in ['coil_short']:
                haze = start_haze(haze_color=(100, 100, 255), haze_duration=1200, alpha=90)
                draw_haze(screen, haze)
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
                    screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)

                pygame.time.set_timer(pygame.USEREVENT + 2, 1000, loops=1)

                screenshake_status = True
                if screenshake_status == True:
                    death_animation(player, screen, clock)
                    deathanim_status = True
                    if deathanim_status == True:
                        show_gameover_screen(screen, gameover_screen)

            elif collided_obstacle.type == 'resistor':
                quick_light_flashes(screen)
                screenshake(screen, player, obstacle_group, current_zone, intensity=8, duration=30)
                screenshake_status = True
                if screenshake_status == True:
                    death_animation(player, screen, clock)
                    deathanim_status = True
                    if deathanim_status == True:
                        show_gameover_screen(screen, gameover_screen)

            elif collided_obstacle.type == 'transformer_up':
                player.sprite.gravity = -40  # accelerate upward*
                transformer_up_sound.play()  # put effect*

            elif collided_obstacle.type == 'transformer_down':
                player.sprite.gravity += 15  # accelerate downward*
                transformer_down_sound.play()  # put effect*
                # Apply screenshake based on current zone*
                screenshake(screen, player, obstacle_group, current_zone, intensity=5, duration=10)

            elif collided_obstacle.type in ['fluxflip_horizontal', 'fluxflip_vertical']:
                if collided_obstacle.type == 'fluxflip_vertical':
                    player.sprite.gravity = -40  # Launch upward like a jump*
                    flux_sound = pygame.mixer.Sound('audio/fluxflip_vertical.wav')
                    flux_sound.set_volume(10)
                    flux_sound.play()
                elif collided_obstacle.type == 'fluxflip_horizontal':
                    player.sprite.velocity_x = 15  # Push player rightward
                    fluxflip_horizontal_sound = pygame.mixer.Sound('audio/fluxflip_horizontal.wav')
                    fluxflip_horizontal_sound.set_volume(10)
                    fluxflip_horizontal_sound.play()

            elif collided_obstacle.type == 'roundabout':
                player.sprite.roundabout_collision(obstacle_group)

            elif collided_obstacle.type == 'signswitcher':
                player.sprite.switch_sign()
                quick_light_flashes(screen, flash_color=(100, 180, 100))

            elif collided_obstacle.type == 'stick':
                player.sprite.stuck_timer = 90
                player.sprite.stick_collision(obstacle_group)

            elif collided_obstacle.type == 'portal':
                quick_light_flashes(screen, flash_color=(100, 180, 255))
                if current_zone == zone_fire:
                    current_zone = zone_ice
                else:
                    current_zone = zone_fire
                obstacle_group.empty()

            collided_obstacle.kill()

        else:
            game_active = True

    else:
        screen.blit(jj_title, (0,0))
        if instruction_step == 1:
            screen.blit(instructions_1, (0, 0))
        elif instruction_step == 2:
            screen.blit(instructions_2, (0, 0))
        elif instruction_step == 3:
            screen.blit(instructions_3, (0, 0))
        elif instruction_step == 4:
            screen.blit(instructions_4, (0, 0))
        elif instruction_step == 5:
            screen.blit(instructions_5, (0, 0))
        elif credits_screen == 1:
            screen.blit(credits_1, (0, 0))


        # score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        # score_message_rect = score_message.get_rect(center = (400,330))
        # screen.blit(game_name,game_name_rect)

        # if score == 0: screen.blit(game_message,game_message_rect)
        # else: screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)




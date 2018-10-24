import pygame
from pygame.sprite import Sprite


class Pacman(Sprite):
    def __init__(self, settings, screen, spritesheet):
        super(Pacman, self).__init__()
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((457, 1, 13, 13), (473, 1, 13, 13), (489, 1, 13, 13),
                            (457, 17, 13, 13), (473, 17, 13, 13), (489, 1, 13, 13),
                            (457, 33, 13, 13), (473, 33, 13, 13), (489, 1, 13, 13),
                            (457, 49, 13, 13), (473, 49, 13, 13), (489, 1, 13, 13),
                            (505, 1, 13, 13), (521, 1, 13, 13), (537, 1, 13, 13), (553, 1, 13, 13), (569, 1, 13, 13),
                            (585, 1, 13, 13), (601, 1, 13, 13), (617, 1, 13, 13), (633, 1, 13, 13), (649, 1, 13, 13),
                            (665, 1, 13, 13))
        self.images = spritesheet.images_at(self.image_rects, settings.entity_width, settings.entity_height,
                                            colorkey=(0, 0, 0))
        self.rect = self.images[0].get_rect()
        self.rect.y = self.settings.block_height * 38 + self.settings.screen_height/8
        self.rect.x = self.screen_rect.centerx - self.settings.block_width * 23 + self.settings.block_width * 21.5

        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.moving_up = False
        self.direction = 1

        self.bullet_active = False
        self.portals_active = False
        self.portal_switch = False
        self.portal_cooldown = 0

        self.image_frame = 0

    def check_space(self, left_collisions, left_collisions2, right_collisions, right_collisions2, up_collisions,
                    up_collisions2, down_collisions, down_collisions2, down_collisions3):
        if (not left_collisions or (left_collisions2 and not right_collisions)) and self.move_left \
                and not self.moving_left:
            self.direction = 0
            self.moving_left = True
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 3
        elif (not right_collisions or (right_collisions2 and not left_collisions)) and self.move_right \
                and not self.moving_right:
            self.direction = 1
            self.moving_left = False
            self.moving_right = True
            self.moving_up = False
            self.moving_down = False
            self.image_frame = 0
        elif (not up_collisions or (up_collisions2 and not down_collisions)) and self.move_up and not self.moving_up:
            self.direction = 2
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 6
        elif (not down_collisions or (down_collisions2 and not up_collisions)) and not down_collisions3 and \
                self.move_down and not self.moving_down:
            self.direction = 3
            self.moving_up = False
            self.moving_down = True
            self.moving_left = False
            self.moving_right = False
            self.image_frame = 9

    def left_block_collide(self):
        self.moving_left = False
        self.rect.x += 1

    def right_block_collide(self):
        self.moving_right = False
        self.rect.x -= 1

    def up_block_collide(self):
        self.moving_up = False
        self.rect.y += 1

    def down_block_collide(self):
        self.moving_down = False
        self.rect.y -= 1

    def update_pacman(self, settings):
        if self.moving_left:
            self.rect.x -= settings.pacman_speed
        elif self.moving_right:
            self.rect.x += settings.pacman_speed
        elif self.moving_up:
            self.rect.y -= settings.pacman_speed
        elif self.moving_down:
            self.rect.y += settings.pacman_speed

    def reset_pacman(self):
        self.rect.top = self.settings.block_height * 37 + self.settings.screen_height/8
        self.rect.left = self.screen_rect.centerx - self.settings.block_width * 23 + self.settings.block_width * 21.5

        self.direction = 1
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.moving_up = False

        self.image_frame = 0

    def draw(self):
        self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self):
        if self.moving_left or self.moving_right or self.moving_up or self.moving_down:
            self.image_frame += 1
            if self.image_frame == 3 and self.moving_right:
                self.image_frame = 0
            elif self.image_frame == 6 and self.moving_left:
                self.image_frame = 3
            elif self.image_frame == 9 and self.moving_up:
                self.image_frame = 6
            elif self.image_frame == 12 and self.moving_down:
                self.image_frame = 9

    def cooldown(self):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1


class LeftHitbox(Sprite):
    def __init__(self, settings, pacman):
        super(LeftHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, 1, settings.entity_height)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.right = pacman.rect.left - 1
        self.rect.top = pacman.rect.top


class RightHitbox(Sprite):
    def __init__(self, settings, pacman):
        super(RightHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, 1, settings.entity_height)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.left = pacman.rect.right + 1
        self.rect.top = pacman.rect.top


class UpHitbox(Sprite):
    def __init__(self, settings, pacman):
        super(UpHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, settings.entity_width, 1)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.left = pacman.rect.left
        self.rect.bottom = pacman.rect.top - 1


class DownHitbox(Sprite):
    def __init__(self, settings, pacman):
        super(DownHitbox, self).__init__()
        self.rect = pygame.Rect(0, 0, settings.entity_width, 1)
        self.update_hitbox(pacman)

    def update_hitbox(self, pacman):
        self.rect.left = pacman.rect.left
        self.rect.top = pacman.rect.bottom + 1

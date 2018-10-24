import pygame
from pygame.sprite import Sprite


class PortalBullet(Sprite):
    def __init__(self, settings, screen, spritesheet, pacman):
        super(PortalBullet, self).__init__()
        self.settings = settings
        self.screen = screen

        self.imagerects = ((624, 18, 4, 4), (630, 18, 4, 4), (636, 18, 4, 4), (642, 18, 4, 4),
                           (624, 24, 4, 4), (630, 24, 4, 4), (636, 24, 4, 4), (642, 24, 4, 4))
        self.images = spritesheet.images_at(self.imagerects, settings.bullet_width, settings.bullet_height,
                                            colorkey=(0, 0, 0))
        self.current_image = None

        self.rect = self.images[0].get_rect()

        self.speed = settings.bullet_speed
        self.direction = pacman.direction
        self.portal_switch = pacman.portal_switch
        self.pacman_rect = pacman.rect

        self.initialize_bullet()

    def initialize_bullet(self):
        if self.direction == 0:
            self.rect.right = self.pacman_rect.left
            self.rect.centery = self.pacman_rect.centery
            if not self.portal_switch:
                self.current_image = self.images[0]
            else:
                self.current_image = self.images[4]
        elif self.direction == 1:
            self.rect.left = self.pacman_rect.right
            self.rect.centery = self.pacman_rect.centery
            if not self.portal_switch:
                self.current_image = self.images[1]
            else:
                self.current_image = self.images[5]
        elif self.direction == 2:
            self.rect.bottom = self.pacman_rect.top
            self.rect.centerx = self.pacman_rect.centerx
            if not self.portal_switch:
                self.current_image = self.images[2]
            else:
                self.current_image = self.images[6]
        elif self.direction == 3:
            self.rect.top = self.pacman_rect.bottom
            self.rect.centerx = self.pacman_rect.centerx
            if not self.portal_switch:
                self.current_image = self.images[3]
            else:
                self.current_image = self.images[7]

    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def update_bullet(self):
        if self.direction == 0:
            self.rect.x -= self.speed
        elif self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == 2:
            self.rect.y -= self.speed
        elif self.direction == 3:
            self.rect.y += self.speed

    def regress(self):
        if self.direction == 0:
            self.rect.x += 1
        elif self.direction == 1:
            self.rect.x -= 1
        elif self.direction == 2:
            self.rect.y += 1
        elif self.direction == 3:
            self.rect.y -= 1


class Portal(Sprite):
    def __init__(self, settings, screen, spritesheet):
        super(Portal, self).__init__()
        self.settings = settings
        self.screen = screen

        self.imagerects1 = ((599, 18, 4, 11), (605, 18, 4, 11))
        self.imagerects2 = ((611, 18, 11, 4), (611, 24, 11, 4))
        self.images = spritesheet.images_at(self.imagerects1, settings.portal_width, settings.portal_length,
                                            colorkey=(0, 0, 0))
        self.images.extend(spritesheet.images_at(self.imagerects2, settings.portal_length, settings.portal_width,
                                                 colorkey=(0, 0, 0)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x -= self.rect.width
        self.portal_direction = None

    def initialize_portal(self, bullet, portal_switch):
        if bullet.direction == 0 or bullet.direction == 1:
            if not portal_switch:
                self.image = self.images[0]
            else:
                self.image = self.images[1]
            self.rect = self.image.get_rect()
            if bullet.direction == 0:
                self.portal_direction = 1
                self.rect.right = bullet.rect.left
            else:
                self.portal_direction = 0
                self.rect.left = bullet.rect.right
            self.rect.centery = bullet.rect.centery
        if bullet.direction == 2 or bullet.direction == 3:
            if not portal_switch:
                self.image = self.images[2]
            else:
                self.image = self.images[3]
            self.rect = self.image.get_rect()
            if bullet.direction == 2:
                self.portal_direction = 3
                self.rect.bottom = bullet.rect.top
            else:
                self.portal_direction = 2
                self.rect.top = bullet.rect.bottom
            self.rect.centerx = bullet.rect.centerx

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def reset_portal(self):
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x -= self.rect.width
        self.portal_direction = None

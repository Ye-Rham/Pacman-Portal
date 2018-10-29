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

        self.portal_active = False
        self.expiration_time = 0

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
        self.portal_active = True
        self.expiration_time = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def reset_portal(self, pacman):
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x -= self.rect.width
        self.portal_direction = None
        self.portal_active = False
        self.expiration_time = 0
        pacman.portals_active = False

    def expire_portal(self, pacman):
        if self.portal_active:
            self.expiration_time += 1
            if self.expiration_time == 60 * 10:
                self.reset_portal(pacman)


class SidePortals:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.left_x = self.screen_rect.centerx - self.settings.block_width * 30.5
        self.right_x = self.screen_rect.centerx + self.settings.block_width * 27.5
        self.y = self.settings.block_height * 27 + self.settings.screen_height * 1/8 + 1
        self.left_rect = pygame.Rect(self.left_x, self.y, settings.entity_width, settings.entity_height)
        self.right_rect = pygame.Rect(self.right_x, self.y, settings.entity_width, settings.entity_height)
        self.color = (0, 0, 0)

    def draw(self):
        self.screen.fill(self.color, self.left_rect)
        self.screen.fill(self.color, self.right_rect)

    def transport(self, entity):
        if entity.rect.left <= self.left_rect.left:
            entity.rect.right = self.right_rect.right - 1
        elif entity.rect.right >= self.right_rect.right:
            entity.rect.left = self.left_rect.left + 1

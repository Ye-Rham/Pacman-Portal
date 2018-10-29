import pygame
from pygame.sprite import Sprite


class Fruit(Sprite):
    def __init__(self, settings, screen, spritesheet):
        super(Fruit, self).__init__()
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image_rects = ((489, 49, 14, 14), (505, 49, 14, 14), (521, 49, 14, 14), (537, 49, 14, 14),
                            (553, 49, 14, 14), (569, 49, 14, 14), (585, 49, 14, 14), (601, 49, 14, 14))
        self.image_rects2 = ((456, 148, 15, 7), (472, 148, 15, 7), (488, 148, 15, 7), (504, 148, 15, 7))
        self.image_rects3 = ((520, 148, 18, 7), (518, 164, 20, 7), (518, 180, 20, 7), (518, 194, 20, 8))
        self.images = (spritesheet.images_at(self.image_rects, settings.entity_width, settings.entity_height,
                                             colorkey=(0, 0, 0)) +
                       spritesheet.images_at(self.image_rects2, settings.text_width * 3, settings.text_height,
                                             colorkey=(0, 0, 0)) +
                       spritesheet.images_at(self.image_rects3, settings.text_width * 4, settings.text_height,
                                             colorkey=(0, 0, 0)))
        self.rect = self.images[0].get_rect()
        self.rect.x = 0 - self.rect.width

        self.time = 0
        self.active = False
        self.expiration_time = 0
        self.text = False
        self.fruit_count = 0

    def update_fruit(self):
        if self.fruit_count < 2:
            self.time += 1
            if self.time == 60 * 30:
                self.rect = self.images[0].get_rect()
                self.rect.centerx = self.screen_rect.centerx
                self.rect.centery = self.settings.block_height * 34.5 + self.settings.screen_height/8
                self.active = True
                self.fruit_count += 1

    def draw(self, score):
        if not self.text and self.active:
            self.screen.blit(self.images[(score.level - 1) % 8], self.rect)
            self.expiration_time += 1
            if self.expiration_time == 60 * 10:
                self.reset_fruit()
        elif self.active:
            self.screen.blit(self.images[(score.level - 1) % 8 + 8], self.rect)
            self.expiration_time += 1
            if self.expiration_time == 60 * 5:
                self.reset_fruit()

    def reset_fruit(self):
            self.rect.x = 0 - self.rect.width
            self.time = 0
            self.active = False
            self.expiration_time = 0
            self.text = False

    def prep_points_image(self, score):
        self.rect = self.images[(score.level - 1) % 8 + 8].get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.settings.block_height * 34.5 + self.settings.screen_height / 8
        self.expiration_time = 0

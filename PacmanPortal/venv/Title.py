import pygame


class Title:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.font = pygame.font.SysFont(None, 72)
        self.image = self.font.render(str("PAC-MAN PORTAL"), True, settings.text_color1)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = settings.screen_height * 1/8

    def draw(self):
        self.screen.blit(self.image, self.rect)

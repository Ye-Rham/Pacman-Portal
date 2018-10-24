import pygame


class Button:
    def __init__(self, settings, screen, msg, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x = x
        self.y = y

        self.width, self.height = 200, 50
        self.button_rect = pygame.Rect(0, 0, self.width, self.height)
        self.button_rect.centerx = x
        self.button_rect.centery = y
        self.button_color = settings.button_color
        self.text_color = settings.text_color1
        self.font = pygame.font.SysFont(None, 36)

        self.msg = msg
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = x
        self.msg_rect.centery = y

    def prep_msg(self):
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = self.x
        self.msg_rect.centery = self.y

    def draw(self):
        self.screen.fill(self.button_color, self.button_rect)
        self.screen.blit(self.msg_image, self.msg_rect)

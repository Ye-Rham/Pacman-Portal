import pygame


class Score:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.points = 0
        self.lives = 3
        self.text_color1 = settings.text_color1
        self.bg_color = settings.bg_color
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.high_score_file = open("High_Scores.txt", "r")
        self.high_score_list = []
        for line in self.high_score_file:
            self.high_score_list.append(int(line))
        self.high_score_file.close()
        if self.high_score_list:
            self.high_score = self.high_score_list[0]
        else:
            self.high_score = 0

        self.score_image1 = self.font.render("SCORE", True, self.text_color1, self.bg_color)
        self.image_rect1 = self.score_image1.get_rect()
        self.image_rect1.centerx = self.screen_rect.centerx
        self.image_rect1.y = 0

        self.score_image2 = self.font.render(str(self.points), True, self.text_color1, self.bg_color)
        self.image_rect2 = self.score_image2.get_rect()
        self.image_rect2.centerx = self.screen_rect.centerx
        self.image_rect2.y = 24

    def prep_score(self):
        self.score_image2 = self.font.render(str(self.points), True, self.text_color1, self.bg_color)
        self.image_rect2 = self.score_image2.get_rect()
        self.image_rect2.centerx = self.screen_rect.centerx
        self.image_rect2.y = 24

    def show_score(self):
        self.screen.blit(self.score_image1, self.image_rect1)
        self.screen.blit(self.score_image2, self.image_rect2)

    def reset_score(self):
        self.points = 0
        self.lives = 3

    def show_high_score_list(self):
        for x in range(0, len(self.high_score_list)):
            self.rect.x, self.rect.y = self.screen_rect.centerx - 60, self.screen_rect.centery / 3 + 10 + x * 48
            self.screen.blit(self.font.render((str(x + 1) + ".   " + str(self.high_score_list[x])), True,
                                              self.text_color1, (0, 0, 0)), self.rect)

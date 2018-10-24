import pygame
from pygame.sprite import Sprite


class Block(Sprite):
    def __init__(self, settings, screen, x, y):
        super(Block, self).__init__()
        self.screen = screen
        self.width = settings.block_width
        self.height = settings.block_height
        self.color = settings.block_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = x
        self.rect.top = y
        self.draw_rect = self.rect
        self.draw_rect.width += 1
        self.draw_rect.height += 1

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.draw_rect)


class GBlock(Sprite):
    def __init__(self, settings, screen, x, y):
        super(GBlock, self).__init__()
        self.screen = screen
        self.width = settings.block_width
        self.height = settings.block_height
        self.color = settings.pellet_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left = x
        self.rect.top = y
        self.draw_rect = self.rect
        self.draw_rect.width += 1
        self.draw_rect.height += 1

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.draw_rect)


class Pellet(Sprite):
    def __init__(self, settings, screen, x, y):
        super(Pellet, self).__init__()
        self.screen = screen
        self.width = settings.pellet_width
        self.height = settings.pellet_height
        self.color = settings.pellet_color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x + settings.block_width/2
        self.rect.centery = y + settings.block_height/2

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class PowerPellet(Sprite):
    def __init__(self, settings, screen, spritesheet, x, y):
        super(PowerPellet, self).__init__()
        self.screen = screen
        self.image_rects = ((8, 24, 8, 8), (0, 0, 1, 1))
        self.images = spritesheet.images_at(self.image_rects, settings.power_pellet_width, settings.power_pellet_height,
                                            colorkey=(0, 0, 0))
        self.rect = self.images[0].get_rect()
        self.rect.centerx = x + settings.block_width/2
        self.rect.centery = y + settings.block_height/2
        self.image_frame = 0

    def draw(self):
        self.screen.blit(self.images[self.image_frame], self.rect)

    def next_frame(self):
        self.image_frame += 1
        if self.image_frame == 2:
            self.image_frame = 0


class Maze:
    def __init__(self, settings, screen, spritesheet, blocks, g_blocks, pellets, power_pellets):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.blueprint = open('MazeCoordinates.txt', "r")
        self.mazematrix = list(self.blueprint)

        self.create_maze(spritesheet, blocks, g_blocks, pellets, power_pellets)

    def create_maze(self, spritesheet, blocks, g_blocks, pellets, power_pellets):
        for y in range(0, len(self.mazematrix)):
            for x in range(0, len(self.mazematrix[y])):
                if self.mazematrix[y][x] == 'X':
                    newblock = Block(self.settings, self.screen,
                                     (self.screen_rect.centerx - self.settings.block_width * 23 +
                                      self.settings.block_width * x),
                                     self.settings.block_height * y + self.settings.screen_height/8)
                    blocks.add(newblock)
                elif self.mazematrix[y][x] == 'G':
                    newg_block = GBlock(self.settings, self.screen,
                                        (self.screen_rect.centerx - self.settings.block_width * 23 +
                                         self.settings.block_width * x),
                                        self.settings.block_height * y + self.settings.screen_height/8)
                    g_blocks.add(newg_block)
                elif self.mazematrix[y][x] == 'p':
                    newpellet = Pellet(self.settings, self.screen,
                                       (self.screen_rect.centerx - self.settings.block_width * 23 +
                                        self.settings.block_width * x),
                                       self.settings.block_height * y + self.settings.screen_height/8)
                    pellets.add(newpellet)
                elif self.mazematrix[y][x] == 'P':
                    newpower_pellet = PowerPellet(self.settings, self.screen, spritesheet,
                                                  (self.screen_rect.centerx - self.settings.block_width * 23 +
                                                   self.settings.block_width * x),
                                                  self.settings.block_height * y + self.settings.screen_height / 8)
                    power_pellets.add(newpower_pellet)

    def reset_maze(self, spritesheet, pellets, power_pellets):
        for y in range(0, len(self.mazematrix)):
            for x in range(0, len(self.mazematrix[y])):
                if self.mazematrix[y][x] == 'p':
                    newpellet = Pellet(self.settings, self.screen,
                                       (self.screen_rect.centerx - self.settings.block_width * 23 +
                                        self.settings.block_width * x),
                                       self.settings.block_height * y + self.settings.screen_height/8)
                    pellets.add(newpellet)
                elif self.mazematrix[y][x] == 'P':
                    newpower_pellet = PowerPellet(self.settings, self.screen, spritesheet,
                                                  (self.screen_rect.centerx - self.settings.block_width * 23 +
                                                   self.settings.block_width * x),
                                                  self.settings.block_height * y + self.settings.screen_height / 8)
                    power_pellets.add(newpower_pellet)

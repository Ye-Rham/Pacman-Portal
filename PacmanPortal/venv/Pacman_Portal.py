import pygame
from pygame.sprite import Group
from time import sleep

from Game_Settings import Settings
from Sprite_Sheet import SpriteSheet
from Score import Score
from Button import Button
from Pacman import Pacman
from Pacman import LeftHitbox
from Pacman import RightHitbox
from Pacman import UpHitbox
from Pacman import DownHitbox
from Portals import Portal
from Maze import Maze
import Game_Functions as gf


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Pacman Portal")
    spritesheet = SpriteSheet('Arcade - Pac-Man - General Sprites.png', screen)
    play_button = Button(settings, screen, "PLAY", settings.screen_width/2, settings.screen_height*2/3)
    score_button = Button(settings, screen, "HIGH SCORES", settings.screen_width/2, settings.screen_height*2/3 + 100)

    score = Score(settings, screen)
    pacman = Pacman(settings, screen, spritesheet)
    orange_portal = Portal(settings, screen, spritesheet)
    blue_portal = Portal(settings, screen, spritesheet)
    left_hitbox = LeftHitbox(settings, pacman)
    right_hitbox = RightHitbox(settings, pacman)
    up_hitbox = UpHitbox(settings, pacman)
    down_hitbox = DownHitbox(settings, pacman)

    blocks = Group()
    g_blocks = Group()
    pellets = Group()
    power_pellets = Group()
    bullets = Group()
    time = 1

    maze = Maze(settings, screen, spritesheet, blocks, g_blocks, pellets, power_pellets)

    while True:
        timer = pygame.time.Clock()
        timer.tick(60)
        time += 1
        if time == 61:
            time = 1
        gf.check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets)
        gf.update_screen(settings, screen, time, score, play_button, score_button, pacman, blocks, g_blocks,
                         pellets, power_pellets, bullets, orange_portal, blue_portal)
        if settings.game_on:
            gf.update_screen(settings, screen, time, score, play_button, score_button, pacman, blocks,
                             g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal)
            sleep(6)
            while settings.game_on:
                timer.tick(60)
                time += 1
                if time == 61:
                    time = 1
                if pacman.portal_cooldown > 0:
                    pacman.portal_cooldown -= 1
                gf.check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets)
                gf.check_collisions(settings, screen, time, spritesheet, score, play_button, score_button,
                                    pacman, maze, blocks, g_blocks, pellets, power_pellets,
                                    left_hitbox, right_hitbox, up_hitbox, down_hitbox, bullets, orange_portal,
                                    blue_portal)
                pacman.update_pacman(settings)
                for bullet in bullets:
                    bullet.update_bullet()
                left_hitbox.update_hitbox(pacman)
                right_hitbox.update_hitbox(pacman)
                up_hitbox.update_hitbox(pacman)
                down_hitbox.update_hitbox(pacman)
                if time % 30 == 0:
                    print('x = ' + str(pacman.rect.x))
                gf.update_screen(settings, screen, time, score, play_button, score_button, pacman, blocks,
                                 g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal)
        elif settings.score_on:
            while settings.score_on:
                gf.check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets)
                gf.update_screen(settings, screen, time, score, play_button, score_button, pacman, blocks,
                                 g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal)


run_game()

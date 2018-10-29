import pygame
from pygame.sprite import Group
from time import sleep

from Game_Settings import Settings
from Sprite_Sheet import SpriteSheet
from Score import Score
from Button import Button
from Title import Title
from Pacman import Pacman
from Pacman import LeftHitbox
from Pacman import RightHitbox
from Pacman import UpHitbox
from Pacman import DownHitbox
from Ghosts import RedGhost
from Portals import Portal
from Portals import SidePortals
from Maze import Maze
from Fruit import Fruit
import Game_Functions as gf


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Pacman Portal")
    spritesheet = SpriteSheet('Arcade - Pac-Man - General Sprites.png', screen)
    title = Title(settings, screen)
    play_button = Button(settings, screen, "PLAY", settings.screen_width/2, settings.screen_height*2/3)
    score_button = Button(settings, screen, "HIGH SCORES", settings.screen_width/2, settings.screen_height*2/3 + 100)

    # http://www.classicgaming.cc/classics/pac-man/sounds
    # https://www.sounds-resource.com/arcade/pacman/sound/10603/
    # https://www.sounds-resource.com/pc_computer/portal/sound/891/
    game_sounds = {"Ready": pygame.mixer.Sound("pacman_beginning.wav"),
                   "EatPellet": pygame.mixer.Sound("Pellet.wav"),
                   "EatFruit": pygame.mixer.Sound("pacman_eatfruit.wav"),
                   "EatGhost": pygame.mixer.Sound("pacman_eatghost.wav"),
                   "ExtraLife": pygame.mixer.Sound("pacman_extrapac.wav"),
                   "Death": pygame.mixer.Sound("pacman_death.wav"),
                   "GhostFloat": pygame.mixer.Sound("ghost_float.wav"),
                   "GhostReturn": pygame.mixer.Sound("ghost_return.wav"),
                   "GhostVulnerable": pygame.mixer.Sound("ghost_vulnerable.wav"),
                   "OrangeBullet": pygame.mixer.Sound("orange_portal_bullet.wav"),
                   "BlueBullet": pygame.mixer.Sound("blue_portal_bullet.wav"),
                   "PortalOpen": pygame.mixer.Sound("portal_open.wav"),
                   "Port": pygame.mixer.Sound("portal_enter.wav")}
    channel1 = pygame.mixer.Channel(1)
    channel2 = pygame.mixer.Channel(2)
    channel3 = pygame.mixer.Channel(3)

    score = Score(settings, screen, spritesheet)
    pacman = Pacman(settings, screen, spritesheet)
    red_ghost = RedGhost(settings, screen, spritesheet)
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
    side_portals = SidePortals(settings, screen)
    fruit = Fruit(settings, screen, spritesheet)
    time = 1

    maze = Maze(settings, screen, spritesheet, blocks, g_blocks, pellets, power_pellets)

    while True:
        timer = pygame.time.Clock()
        timer.tick(60)
        time += 1
        if time == 61:
            time = 1
        gf.update_screen(settings, screen, time, score, title, play_button, score_button, pacman, blocks, g_blocks,
                         pellets, power_pellets, bullets, orange_portal, blue_portal, fruit, side_portals,
                         red_ghost)
        gf.check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets, game_sounds,
                        channel3)
        if settings.game_on:
            pygame.mouse.set_visible(False)
            maze.reset_maze(spritesheet, pellets, power_pellets)
            pacman.reset_pacman()
            red_ghost.reset_ghost()
            fruit.reset_fruit()
            fruit.fruit_count = 0
            bullets.empty()
            orange_portal.reset_portal(pacman)
            blue_portal.reset_portal(pacman)
            score.reset_score()
            score.prep_lives()
            score.prep_score()
            score.prep_high_score()
            score.prep_level()
            gf.update_screen(settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                             g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal, fruit, side_portals,
                             red_ghost)
            maze.pre_game_draw()
            channel1.play(game_sounds["Ready"])
            sleep(5)
            while settings.game_on:
                timer.tick(60)
                time += 1
                if time == 61:
                    time = 1
                pacman.cooldown()
                red_ghost.cooldown()
                gf.check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets, game_sounds,
                                channel3)
                if pacman.active:
                    gf.check_collisions(settings, score, pacman, blocks, g_blocks, pellets, power_pellets, left_hitbox,
                                        right_hitbox, up_hitbox, down_hitbox, bullets, orange_portal, blue_portal,
                                        fruit, game_sounds, channel1, channel2, channel3, side_portals, red_ghost)
                score.extra_life(game_sounds, channel2)

                if not pacman.active and not channel1.get_sound() and score.lives > 0:
                    score.lives -= 1
                    score.prep_lives()
                    pacman.reset_pacman()
                    red_ghost.reset_ghost()
                    fruit.reset_fruit()
                    fruit.fruit_count = 0
                    bullets.empty()
                    orange_portal.reset_portal(pacman)
                    blue_portal.reset_portal(pacman)
                    sleep(3)
                    gf.update_screen(settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                                     g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal, fruit,
                                     side_portals, red_ghost)
                    maze.pre_game_draw()
                    sleep(5)
                elif not pacman.active and not channel1.get_sound() and score.lives == 0:
                    sleep(3)
                    settings.game_on = False
                    pygame.mouse.set_visible(True)
                    for x in range(0, len(score.high_score_list)):
                        if score.points > score.high_score_list[x]:
                            score.high_score_list.insert(x, score.points)
                            score.high_score_list.pop()
                            break
                    high_score_file = open("High_Scores.txt", "w")
                    for x in range(0, len(score.high_score_list) - 1):
                        high_score_file.write(str(score.high_score_list[x]) + "\n")
                    high_score_file.write(str(score.high_score_list[8]))
                    high_score_file.close()
                    print(list(map(str, score.high_score_list)))

                pacman.update_pacman()
                red_ghost.update_ghost(pacman)
                for bullet in bullets:
                    bullet.update_bullet()
                left_hitbox.update_hitbox(pacman)
                right_hitbox.update_hitbox(pacman)
                up_hitbox.update_hitbox(pacman)
                down_hitbox.update_hitbox(pacman)
                orange_portal.expire_portal(pacman)
                blue_portal.expire_portal(pacman)
                fruit.update_fruit()
                if not channel2.get_sound():
                    channel2.play(game_sounds["GhostFloat"])

                gf.update_screen(settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                                 g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal, fruit,
                                 side_portals, red_ghost)

                if len(pellets) == 0 and len(power_pellets) == 0:
                    gf.end_level(settings, screen, time, spritesheet, score, title, play_button, score_button, pacman,
                                 maze, blocks, g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal,
                                 fruit, channel1, channel2, channel3, side_portals, red_ghost)
        elif settings.score_on:
            while settings.score_on:
                gf.check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets, game_sounds,
                                channel3)
                gf.update_screen(settings, screen, time, score, title, play_button, score_button, pacman, blocks,
                                 g_blocks, pellets, power_pellets, bullets, orange_portal, blue_portal, fruit,
                                 side_portals, red_ghost)


run_game()

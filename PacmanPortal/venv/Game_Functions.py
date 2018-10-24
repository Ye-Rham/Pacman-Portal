import pygame
from pygame.sprite import Group
from time import sleep
import sys
from Portals import PortalBullet


def check_keydown_events(event, settings, screen, spritesheet, pacman, bullets):
    if event.key == pygame.K_LEFT:
        pacman.move_left = True
    elif event.key == pygame.K_RIGHT:
        pacman.move_right = True
    elif event.key == pygame.K_UP:
        pacman.move_up = True
    elif event.key == pygame.K_DOWN:
        pacman.move_down = True
    elif event.key == pygame.K_SPACE:
        if not pacman.bullet_active:
            bullet = PortalBullet(settings, screen, spritesheet, pacman)
            bullets.add(bullet)
            pacman.bullet_active = True


def check_keyup_events(event, pacman):
    if event.key == pygame.K_LEFT:
        pacman.move_left = False
    elif event.key == pygame.K_RIGHT:
        pacman.move_right = False
    elif event.key == pygame.K_UP:
        pacman.move_up = False
    elif event.key == pygame.K_DOWN:
        pacman.move_down = False


def check_events(settings, screen, spritesheet, play_button, score_button, pacman, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and settings.game_on:
            check_keydown_events(event, settings, screen, spritesheet, pacman, bullets)
        if event.type == pygame.KEYUP and settings.game_on:
            check_keyup_events(event, pacman)
        if event.type == pygame.MOUSEBUTTONDOWN and not settings.game_on:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, play_button, pacman, mouse_x, mouse_y)
            check_score_button(settings, score_button, mouse_x, mouse_y)


def check_play_button(settings, play_button, pacman, mouse_x, mouse_y):
    if play_button.button_rect.collidepoint(mouse_x, mouse_y):
        settings.game_on = True
        pacman.reset_pacman()


def check_score_button(settings, score_button, mouse_x, mouse_y):
    clicked = score_button.button_rect.collidepoint(mouse_x, mouse_y)
    if clicked and not settings.score_on:
        settings.score_on = True
        score_button.msg = 'BACK'
        score_button.prep_msg()
    elif clicked and settings.score_on:
        settings.score_on = False
        score_button.msg = 'HIGH SCORES'
        score_button.prep_msg()


def check_collisions(settings, screen, time, spritesheet, score, play_button, score_button,
                     pacman, maze, blocks, g_blocks, pellets, power_pellets,
                     left_hitbox, right_hitbox, up_hitbox, down_hitbox, bullets, orange_portal, blue_portal):
    pacmans = Group()
    pacmans.add(pacman)
    left_hits = Group()
    left_hits.add(left_hitbox)
    right_hits = Group()
    right_hits.add(right_hitbox)
    up_hits = Group()
    up_hits.add(up_hitbox)
    down_hits = Group()
    down_hits.add(down_hitbox)
    portals = Group()
    portals.add(orange_portal)
    portals.add(blue_portal)

    pacman_collisions(settings, score, blocks, g_blocks, pellets, power_pellets, pacman, pacmans, left_hitbox,
                      left_hits, right_hitbox, right_hits, up_hitbox, up_hits, down_hitbox, down_hits, orange_portal,
                      blue_portal, portals)

    bullet_collisions(pacman, blocks, g_blocks, bullets, orange_portal, blue_portal, portals)

    score.prep_score()

    if len(pellets) == 0 and len(power_pellets) == 0:
        maze.reset_maze(spritesheet, pellets, power_pellets)
        pacman.reset_pacman()
        bullets.empty()
        for portal in portals:
            portal.reset_portal()
        sleep(3)
        update_screen(settings, screen, time, score, play_button, score_button, pacman, blocks, g_blocks, pellets,
                      power_pellets, orange_portal, blue_portal, portals)
        settings.pacman_speed *= settings.speed_multiplier
        sleep(3)


def pacman_collisions(settings, score, blocks, g_blocks, pellets, power_pellets, pacman, pacmans, left_hitbox,
                      left_hits, right_hitbox, right_hits, up_hitbox, up_hits, down_hitbox, down_hits,
                      orange_portal, blue_portal, portals):
    collisions1 = pygame.sprite.groupcollide(pacmans, pellets, False, True)
    collisions2 = pygame.sprite.groupcollide(pacmans, power_pellets, False, True)
    left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
    left_collisions2 = pygame.sprite.groupcollide(left_hits, portals, False, False)
    right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
    right_collisions2 = pygame.sprite.groupcollide(right_hits, portals, False, False)
    up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
    up_collisions2 = pygame.sprite.groupcollide(up_hits, portals, False, False)
    down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
    down_collisions2 = pygame.sprite.groupcollide(down_hits, portals, False, False)
    down_collisions3 = pygame.sprite.groupcollide(down_hits, g_blocks, False, False)
    orange_portal_collision = pygame.sprite.collide_rect(pacman, orange_portal)
    blue_portal_collision = pygame.sprite.collide_rect(pacman, blue_portal)

    if collisions1:
        for pellets in collisions1.values():
            score.points += settings.pellet_value * len(pellets)
    if collisions2:
        for power_pellets in collisions2.values():
            score.points += settings.pellet_value * len(power_pellets)

    pacman.check_space(left_collisions, left_collisions2, right_collisions, right_collisions2, up_collisions,
                       up_collisions2, down_collisions, down_collisions2, down_collisions3)

    if orange_portal_collision:
        if pacman.portal_cooldown == 0:
            portal_transfer(pacman, blue_portal)
    elif blue_portal_collision:
        if pacman.portal_cooldown == 0:
            portal_transfer(pacman, orange_portal)
    elif left_collisions and not (left_collisions2 and pacman.portals_active) and pacman.moving_left:
        while left_collisions:
            pacman.left_block_collide()
            left_hitbox.update_hitbox(pacman)
            left_collisions = pygame.sprite.groupcollide(left_hits, blocks, False, False)
        pacman.rect.x -= 2
    elif right_collisions and not (right_collisions2 and pacman.portals_active) and pacman.moving_right:
        while right_collisions:
            pacman.right_block_collide()
            right_hitbox.update_hitbox(pacman)
            right_collisions = pygame.sprite.groupcollide(right_hits, blocks, False, False)
        pacman.rect.x += 2
    elif up_collisions and not (up_collisions2 and pacman.portals_active) and pacman.moving_up:
        while up_collisions:
            pacman.up_block_collide()
            up_hitbox.update_hitbox(pacman)
            up_collisions = pygame.sprite.groupcollide(up_hits, blocks, False, False)
        pacman.rect.y -= 2
    elif down_collisions and not (down_collisions2 and pacman.portals_active) and pacman.moving_down:
        while down_collisions:
            pacman.down_block_collide()
            down_hitbox.update_hitbox(pacman)
            down_collisions = pygame.sprite.groupcollide(down_hits, blocks, False, False)
        pacman.rect.y += 2


def portal_transfer(pacman, exit_portal):
    if exit_portal.portal_direction == 0:
        pacman.rect.right = exit_portal.rect.right
        pacman.rect.y = exit_portal.rect.y
        pacman.direction = 0
        pacman.moving_left = True
        pacman.moving_right = False
        pacman.moving_up = False
        pacman.moving_down = False
        pacman.image_frame = 3
    elif exit_portal.portal_direction == 1:
        pacman.rect.left = exit_portal.rect.left
        pacman.rect.y = exit_portal.rect.y
        pacman.direction = 1
        pacman.moving_left = False
        pacman.moving_right = True
        pacman.moving_up = False
        pacman.moving_down = False
        pacman.image_frame = 0
    elif exit_portal.portal_direction == 2:
        pacman.rect.bottom = exit_portal.rect.bottom
        pacman.rect.x = exit_portal.rect.x
        pacman.direction = 2
        pacman.moving_up = True
        pacman.moving_down = False
        pacman.moving_left = False
        pacman.moving_right = False
        pacman.image_frame = 6
    elif exit_portal.portal_direction == 3:
        pacman.rect.top = exit_portal.rect.top
        pacman.rect.x = exit_portal.rect.x
        pacman.direction = 3
        pacman.moving_up = False
        pacman.moving_down = True
        pacman.moving_left = False
        pacman.moving_right = False
        pacman.image_frame = 9
    pacman.portal_cooldown = 15


def bullet_collisions(pacman, blocks, g_blocks, bullets, orange_portal, blue_portal, portals):
    collisions1 = pygame.sprite.groupcollide(blocks, bullets, False, False)
    collisions2 = pygame.sprite.groupcollide(portals, bullets, False, False)
    copy_portal_rect = None
    copy_portal_image = None
    if collisions2:
        bullets.empty()
        pacman.bullet_active = False
    elif collisions1:
        while collisions1:
            for bullet in bullets:
                bullet.regress()
            collisions1 = pygame.sprite.groupcollide(blocks, bullets, False, False)
        for bullet in bullets:
            if not pacman.portal_switch:
                copy_portal_rect = orange_portal.rect
                copy_portal_image = orange_portal.image
                orange_portal.initialize_portal(bullet, pacman.portal_switch)
            else:
                copy_portal_rect = blue_portal.rect
                copy_portal_image = blue_portal.image
                blue_portal.initialize_portal(bullet, pacman.portal_switch)
        portals.empty()
        portals.add(orange_portal)
        portals.add(blue_portal)
        collisions3 = pygame.sprite.groupcollide(portals, g_blocks, False, False)
        bullets.empty()
        pacman.bullet_active = False
        if not collisions3:
            if not pacman.portal_switch:
                pacman.portal_switch = True
            else:
                pacman.portal_switch = False
                pacman.portals_active = True
        else:
            if not pacman.portal_switch:
                orange_portal.rect = copy_portal_rect
                orange_portal.image = copy_portal_image
            else:
                blue_portal.rect = copy_portal_rect
                blue_portal.image = copy_portal_image


def update_screen(settings, screen, time, score, play_button, score_button, pacman, blocks, g_blocks, pellets,
                  power_pellets, bullets, orange_portal, blue_portal):
    if not settings.game_on and not settings.score_on:
        screen.fill(settings.bg_color)
        play_button.draw()
        score_button.draw()
    elif settings.game_on:
        screen.fill(settings.bg_color)
        draw_maze(blocks, g_blocks, pellets, power_pellets)
        pacman.draw()
        for bullet in bullets:
            bullet.draw()
        orange_portal.draw()
        blue_portal.draw()
        score.show_score()
        if time % 3 == 0:
            pacman.next_frame()
        if time % 30 == 0:
            for power_pellet in power_pellets:
                power_pellet.next_frame()
    elif settings.score_on:
        screen.fill(settings.bg_color)
        score.show_high_score_list()
        score_button.draw()
    pygame.display.flip()


def draw_maze(blocks, g_blocks, pellets, power_pellets):
    for block in blocks.sprites():
        block.draw()
    for g_block in g_blocks.sprites():
        g_block.draw()
    for pellet in pellets.sprites():
        pellet.draw()
    for power_pellet in power_pellets.sprites():
        power_pellet.draw()

from time import sleep

import pygame
import classes

pygame.init()

back = (200, 255, 255)  # background color
mw = pygame.display.set_mode((500, 500))  # main window
mw.fill(back)
clock = pygame.time.Clock()

# platform coordinates
racket_x = 200
racket_y = 330
# ---------------------------------------------------------
# end game flag
game_over = False

# create objects: ball and platform
ball = classes.Ball('ball.png', 160, 200, 50, 50)
platform = classes.Platform('platform.png', racket_x, racket_y, 250, 35)
end_label = classes.Picture('end.png', 125, 125, 300, 300)
go_label = classes.Picture('go_sign.png', 0, 0, 500, 500)
ready = classes.Picture('ready.png', 0, 0, 500, 500)

# create enemies
start_x = 5  # first enemy coords
start_y = 5
enemies_count = 9  # enemies in the first raw
enemies = []  # enemies list

for j in range(3):  # create enemies cycle
    y_coord = start_y + (55 * j)  # shift every next raw on 55 px by axis y
    x_coord = start_x + (27.5 * j)  # and 27.5 by x

    for i in range(enemies_count):  # create raw of enemies same as count
        enemy = classes.Enemy('enemy.png', x_coord, y_coord, 50, 50)
        enemies.append(enemy)  # add to list
        x_coord += 55  # next enemy x coordinate
    enemies_count -= 1  # reduce next raw on 1 enemy

# start game cycle
ready.draw(mw)
pygame.display.update()
sleep(2)
mw.fill(back)
go_label.draw(mw)
pygame.display.update()
sleep(2)
mw.fill(back)

while not game_over:
    ball.fill(mw)
    platform.fill(mw)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        # -------------------------------------------
        # Check buttons and change move flags
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                platform.moving_right = True
            if event.key == pygame.K_LEFT:
                platform.moving_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                platform.moving_right = False
            if event.key == pygame.K_LEFT:
                platform.moving_left = False
            # -----------------------------------------
    # Moving objects
    platform.move()
    ball.move()
    # check minimal y_coordinate
    if ball.rect.y > 350 or len(enemies) == 0:
        enemies = []
        mw.fill(back)
        end_label.fill(mw)
        end_label.draw(mw)
        pygame.display.update()
        sleep(2)
        game_over = True
    # ----------------------------------------
    # check if ball touch the platform and change direction:
    ball.check_hit(platform)
    # ----------------------------------------
    # draw enemies from the list
    for enemy in enemies:
        enemy.draw(mw)
    # ---------------------------------------
    # check if the ball has the same coordinates as enemy and killed him
        enemy.check_death(mw, ball, enemies)
    # draw platform and ball
    platform.draw(mw)
    ball.draw(mw)
    # renew scene
    pygame.display.update()
    clock.tick(40)

pygame.quit()
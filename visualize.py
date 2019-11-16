# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
pygame.init()

# Set up the drawing window
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

transparent = (0, 0, 0, 0)

background_image = pygame.image.load("images/road.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (900, 900))

right_axis = 452
left_axis = 410
up_axis = 452
down_axis = 410

right_start = 0
left_start = 900
up_start = 900
down_start = 0

car = pygame.image.load("images/car.png").convert_alpha()
left_car = [pygame.transform.scale(car, (75, 40)), [left_start, left_axis]]
right_car = [pygame.transform.flip(left_car[0], True, False), [right_start, right_axis]]
down_car = [pygame.transform.rotate(left_car[0], 90), [down_axis, down_start]]
up_car = [pygame.transform.flip(down_car[0], False, True), [up_axis, up_start]]

red_light = pygame.image.load("images/redlight.png").convert_alpha()
green_light = pygame.image.load("images/greenlight.png").convert_alpha()
right_red = pygame.transform.scale(red_light, (60, 60))
right_green = pygame.transform.scale(green_light, (60, 60))
left_red = pygame.transform.flip(right_red, False, True)
left_green = pygame.transform.flip(right_green, False, True)
down_red = pygame.transform.rotate(left_red, 90)
down_green = pygame.transform.rotate(left_green, 90)
up_red = pygame.transform.rotate(right_red, 90)
up_green = pygame.transform.rotate(right_green, 90)

left_light_pos = (350, 400)
right_light_pos = (490, 440)
up_light_pos = (440, 360)
down_light_pos = (400, 490)

screen.blit(right_green, left_light_pos)
screen.blit(left_green, right_light_pos)
screen.blit(up_red, up_light_pos)
screen.blit(down_red, down_light_pos)

screen.fill([0,150,50])
screen.blit(background_image, [0, 0])

screen.blit(right_car[0], right_car[1])
screen.blit(left_car[0], left_car[1])
screen.blit(down_car[0], down_car[1])
screen.blit(up_car[0], up_car[1])

pygame.display.update()

# Run until the user asks to quit
running = True
print('running')
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Flip the display
    pygame.display.update()

    # Update and wait
    right_car[1][0] += random.randint(10,30)
    left_car[1][0] -= random.randint(10,30)
    up_car[1][1] -= random.randint(10,30)
    down_car[1][1] += random.randint(10,30)

    if right_car[1][0] > SCREEN_WIDTH:
        right_car[1][0] = right_start
    if left_car[1][0] < 0:
        left_car[1][0] = left_start
    if up_car[1][1] < 0:
        up_car[1][1] = up_start
    if down_car[1][1] > SCREEN_HEIGHT:
        down_car[1][1] = down_start

    screen.fill([0,150,50])
    screen.blit(background_image, [0, 0])

    screen.blit(right_car[0], right_car[1])
    screen.blit(left_car[0], left_car[1])
    screen.blit(down_car[0], down_car[1])
    screen.blit(up_car[0], up_car[1])
    pygame.time.delay(100)

# Done! Time to quit.
pygame.quit()

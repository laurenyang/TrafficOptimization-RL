# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((900,900))

background_image = pygame.image.load("images/road.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (900, 900))

car = pygame.image.load("images/car.png").convert_alpha()
left_car = pygame.transform.scale(car, (75, 40)) 
right_car = pygame.transform.flip(left_car, True, False)
up_car = pygame.transform.rotate(left_car, 90)
down_car = pygame.transform.flip(up_car, False, True)

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

screen.fill([0,150,50])
screen.blit(background_image, [0, 0])

screen.blit(right_car, [600,452])
screen.blit(left_car, [0,410])

screen.blit(down_car, [452, 600])
screen.blit(up_car, [410, 0])

screen.blit(right_green, [490,440])
screen.blit(left_green, [350,400])

screen.blit(up_red, [440,360])
screen.blit(down_red, [400,490])

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

# Done! Time to quit.
pygame.quit()

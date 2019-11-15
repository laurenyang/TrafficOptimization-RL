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

screen.fill([0,255,0])
screen.blit(background_image, [0, 0])

screen.blit(right_car, [600,452])
screen.blit(left_car, [0,410])

screen.blit(down_car, [452, 600])
screen.blit(up_car, [410, 0])


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

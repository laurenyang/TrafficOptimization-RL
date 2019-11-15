# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((900,900))
pygame.display.flip()

background_image = pygame.image.load("images/road.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (900, 900))

car = pygame.image.load("images/car.png").convert_alpha()
car = pygame.transform.scale(car, (75, 40)) 

screen.fill([0,255,0])
screen.blit(background_image, [0, 0])

screen.blit(car, [450,452])
screen.blit(car, [0,412])

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
    # pygame.display.update()

# Done! Time to quit.
pygame.quit()

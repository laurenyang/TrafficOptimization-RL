import pygame
import car
import cargenerate
import trafficlight

class Visualize:
    # Constants
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 900
    ROAD_WIDTH = 100
    CAR_LENGTH = 60
    CAR_WIDTH = 32
    LIGHT_WIDTH = 24
    LIGHT_HEIGHT = 60
    BACKGROUND_COLOR = [0, 150, 50]

    RIGHT_AXIS = SCREEN_HEIGHT // 2 + ROAD_WIDTH // 4 - CAR_WIDTH // 2
    LEFT_AXIS = SCREEN_HEIGHT // 2 - ROAD_WIDTH // 4 - CAR_WIDTH // 2
    UP_AXIS = SCREEN_WIDTH // 2 + ROAD_WIDTH // 4 - CAR_WIDTH // 2
    DOWN_AXIS = SCREEN_WIDTH // 2 - ROAD_WIDTH // 4 - CAR_WIDTH // 2

    RIGHT_START = 0
    LEFT_START = SCREEN_WIDTH - CAR_LENGTH
    UP_START = SCREEN_HEIGHT - CAR_LENGTH
    DOWN_START = 0

    LEFT_LIGHT_POS = (SCREEN_WIDTH // 2 - ROAD_WIDTH // 2 - LIGHT_WIDTH, SCREEN_WIDTH // 2 - ROAD_WIDTH // 2)
    RIGHT_LIGHT_POS = (SCREEN_WIDTH // 2 + ROAD_WIDTH // 2, SCREEN_WIDTH // 2 + ROAD_WIDTH // 2 - LIGHT_HEIGHT)
    UP_LIGHT_POS = (SCREEN_WIDTH // 2 + ROAD_WIDTH // 2 - LIGHT_HEIGHT, SCREEN_WIDTH // 2 - ROAD_WIDTH // 2 - LIGHT_WIDTH)
    DOWN_LIGHT_POS = (SCREEN_HEIGHT // 2 - ROAD_WIDTH // 2, SCREEN_HEIGHT // 2 + ROAD_WIDTH // 2)

    def __init__(self):
        """
        Initialize the visualization screen.
        """
        self.pygame = pygame
        self.pygame.init()
        
        self.screen = self.pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.background_image = self.pygame.image.load("images/road.png").convert_alpha()
        self.background_image = self.pygame.transform.scale(self.background_image, (900, 900))

        self.car = self.pygame.image.load("images/car.png").convert_alpha()
        self.left_car = [self.pygame.transform.scale(self.car, (self.CAR_LENGTH, self.CAR_WIDTH)), [self.LEFT_START, self.LEFT_AXIS]]
        self.right_car = [self.pygame.transform.flip(self.left_car[0], True, False), [self.RIGHT_START, self.RIGHT_AXIS]]
        self.down_car = [self.pygame.transform.rotate(self.left_car[0], 90), [self.DOWN_AXIS, self.DOWN_START]]
        self.up_car = [self.pygame.transform.flip(self.down_car[0], False, True), [self.UP_AXIS, self.UP_START]]

        self.red_light = self.pygame.image.load("images/redlight.png").convert_alpha()
        self.green_light = self.pygame.image.load("images/greenlight.png").convert_alpha()
        self.right_red = self.pygame.transform.scale(self.red_light, (self.LIGHT_WIDTH, self.LIGHT_HEIGHT))
        self.right_green = self.pygame.transform.scale(self.green_light, (self.LIGHT_WIDTH, self.LIGHT_HEIGHT))
        self.left_red = self.pygame.transform.flip(self.right_red, False, True)
        self.left_green = self.pygame.transform.flip(self.right_green, False, True)
        self.down_red = self.pygame.transform.rotate(self.left_red, 90)
        self.down_green = self.pygame.transform.rotate(self.left_green, 90)
        self.up_red = self.pygame.transform.rotate(self.right_red, 90)
        self.up_green = self.pygame.transform.rotate(self.right_green, 90)

        self.screen.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.background_image, [0, 0])

        self.screen.blit(self.right_green, self.RIGHT_LIGHT_POS)
        self.screen.blit(self.left_green, self.LEFT_LIGHT_POS)
        self.screen.blit(self.up_red, self.UP_LIGHT_POS)
        self.screen.blit(self.down_red, self.DOWN_LIGHT_POS)

        self.pygame.display.update()

    def quit(self):
        """
        Ends the pygame instance
        """
        self.pygame.quit()

    def delay(self, time):
        """
        Delays window by time milliseconds
        """
        self.pygame.time.delay(time)

    def update(self, left_cars, right_cars, up_cars, down_cars):
        """
        Updates cars in window
        """
        self.screen.fill([0,150,50])
        self.screen.blit(self.background_image, [0, 0])

        # Add cars moving to the right to the screen
        for car in right_cars:
            self.right_car[1][0] = int(car.pos[0] / 0.25 * self.SCREEN_WIDTH / 2) + self.SCREEN_WIDTH / 2
            self.screen.blit(self.right_car[0], self.right_car[1])

        # Add cars moving to the left to the screen
        for car in left_cars:
            self.left_car[1][0] = int(car.pos[0] / 0.25 * self.SCREEN_WIDTH / 2) + self.SCREEN_WIDTH / 2
            self.screen.blit(self.left_car[0], self.left_car[1])

        # Add cars moving downwards to the screen
        for car in down_cars:
            self.down_car[1][1] = int(car.pos[1] / 0.25 * self.SCREEN_HEIGHT / 2) + self.SCREEN_HEIGHT / 2
            self.screen.blit(self.down_car[0], self.down_car[1])

        # Add cars moving upwards to the screen
        for car in up_cars:
            self.up_car[1][1] = int(car.pos[1] / 0.25 * self.SCREEN_HEIGHT / 2) + self.SCREEN_HEIGHT / 2
            self.screen.blit(self.up_car[0], self.up_car[1])

        self.screen.blit(self.right_green, self.RIGHT_LIGHT_POS)
        self.screen.blit(self.left_green, self.LEFT_LIGHT_POS)
        self.screen.blit(self.down_red, self.DOWN_LIGHT_POS)
        self.screen.blit(self.up_red, self.UP_LIGHT_POS)

        self.pygame.display.update()

def main():
    LEFT_DIR = 0
    UP_DIR = 1
    RIGHT_DIR = 2
    DOWN_DIR = 3
    p = 0.1
    l_car_gen = cargenerate.CarGenerator(LEFT_DIR, p)
    r_car_gen = cargenerate.CarGenerator(RIGHT_DIR, p)
    u_car_gen = cargenerate.CarGenerator(UP_DIR, p)
    d_car_gen = cargenerate.CarGenerator(DOWN_DIR, p)
    lights = trafficlight.TrafficLight([0,0,0,0])

    vis = Visualize()
    l = r = u = d = []
    for i in range(10000):
        l_car = l_car_gen.gen_car(i)
        if l_car:
            l.append(l_car)
        r_car = r_car_gen.gen_car(i)
        if r_car:
            r.append(r_car)
        u_car = u_car_gen.gen_car(i)
        if u_car:
            u.append(u_car)
        d_car = d_car_gen.gen_car(i)
        if d_car:
            d.append(d_car)
        vis.update(l,r,u,d)
        for c in l + r + u + d:
            c.updatePosition(l + r + u + d, lights)
    vis.quit()

if __name__ == "__main__":
    main()
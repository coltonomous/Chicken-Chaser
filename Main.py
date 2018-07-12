#!python2
import random, Obstacles, Menus
from Assets import *


def game_loop():
    """ Main game loop. Contains event handling for crashes, moving between menus,
     and score-keeping."""

    # Defines object starting positions.
    chicken_x = random.randrange(25, aspect_ratio[0] - 100)
    chicken_y = -aspect_ratio[1]
    vehicle_x = aspect_ratio[0] * 0.455
    vehicle_y = aspect_ratio[1] * 0.75

    # Defines object rectangles for collision detection.
    chicken = Obstacles.Chicken(game_display, chicken_x, chicken_y, 74, 74)
    car = Obstacles.Vehicle(game_display, vehicle_x, vehicle_y, 81, 240)

    # Vertical displacement of chicken with each frame.
    chicken_speed = aspect_ratio[1] * 0.00833

    # Continuously updating score for the game.
    score = 0

    # Sets maximum number of chickens that will appear in the game.
    chicken_count = 30

    while chicken_count >= 0:

        # Controls event handling for quitting and car movement.
        for event in pygame.event.get():
            Menus.quit_game(event)
            car.move(event)

        # Adds a hard cap to the chicken speed.
        if chicken_speed < 0.02 * aspect_ratio[1]:
            chicken_speed += 0.00075 * aspect_ratio[1]

        chicken.move(chicken_speed)

        # Handles scoring conditions.
        if chicken.collide(car):
            if score >= 50:
                score -= 50
            else:
                score = 0
        elif car.xpos < chicken.xpos < car.xpos + car.width or \
                car.xpos < chicken.xpos + chicken.width + car.xpos + car.width:
            score += int(30 ** (1 / (car.ypos - (chicken.ypos + chicken.height))))

        # Draws everything to the game display and updates chicken_count.
        game_display.blit(background, (0, 0))
        chicken_count = chicken.spawn(chicken_count)
        chicken.draw()
        car.draw()

        # Updates the surface display.
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    game_loop()

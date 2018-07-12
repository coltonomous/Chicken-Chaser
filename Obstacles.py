import random
from Assets import *


class Obstacles:
    """ Class defines general behavior and attributes of all rectangular moving parts
    in the game."""

    def __init__(self, display, xpos, ypos, width, height):
        """ Defines a pygame rect based on xpos, ypos, width, and height."""

        # To pass display surface to methods for drawing purposes.
        self.display = display

        # Defines Obstacles rectangle.
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.rect_type = pygame.Rect(self.xpos, self.ypos, self.width, self.height)

    def collide(self, other):
        """ Accepts an 'other' Obstacles objects and returns true if it overlaps
        with this one. Returns false otherwise."""

        return self.rect_type.colliderect(other.rect_type)


class Chicken(Obstacles):
    """ Class refines behavior of Obstacles to handle drawing and behavior of
    chickens."""

    def __init__(self, display, xpos, ypos, width, height):
        """ Inherits init from Obstacles and adds a hit variable to track if a Chicken
        has collided with another object. """

        Obstacles.__init__(self, display, xpos, ypos, width, height)

        # Determines how the Obstacle is displayed - chicken or blood splatter.
        self.hit = False

    def draw(self):
        """ Draws self to display surface at self's xpos and ypos. Draws a blood splatter if
        self has collided with another rect. Draws a chicken otherwise."""

        if self.hit:
            self.display.blit(blood_splatter, (self.xpos, self.ypos))
        else:
            self.display.blit(chicken_sprite, (self.xpos + (self.width / 3), self.ypos))

    def collide(self, other):
        """ Accepts an 'other' Obstacles object and returns true if it overlaps
        with this one. Returns false otherwise. Also changes hit field accordingly."""

        collided = Obstacles.collide(self, other)
        self.hit = collided
        return collided

    def spawn(self, count):
        """ If chicken drops below screen, moves chicken back to top at a random
        x position. and resets hit parameter. Also returns passed count of how many
        chickens are remaining in the game."""

        if self.ypos > aspect_ratio[1]:
            self.ypos = 0 - self.height
            self.xpos = random.randrange(random.randrange(25, aspect_ratio[0] - 100))
            self.hit = False
            count -= 1

        return count

    def move(self, speed):
        """ Updates the vertical position of self by shifting downward by number of pixels
        equal to speed."""

        self.ypos += speed
        self.rect_type = pygame.Rect(self.xpos, self.ypos, self.width, self.height)


class Eggs(Chicken):
    """ Class refines behavior of Chicken to handle drawing and behavior of eggs."""

    def __init__(self, display, xpos, ypos, width, height):
        """ Inherits init from chicken verbatim."""

        Chicken.__init__(self, display, xpos, ypos, width, height)

    def draw(self):
        """ Draws self to display surface at self's xpos and ypos. Draws an egg splatter if
        self has collided with another rect. Draws an egg otherwise."""

        # TODO: Add eggs to the game that give bonus points when collided with.
        pass


class Vehicle(Obstacles):
    """ Class refines behavior of Obstacles to handle drawing and controlling of
    vehicles. """

    def __init__(self, display, xpos, ypos, width, height):
        """ Inherits init from Obstacles and adds an xchange attribute to track lateral
        position of the vehicle."""

        Obstacles.__init__(self, display, xpos, ypos, width, height)

        # Determines the horizontal position of the vehicle.
        self.xchange = 0

    def draw(self):
        """ Draws self to display surface at (xpos, ypos)."""

        self.xpos += self.xchange
        self.display.blit(car_sprite, (self.xpos, self.ypos))

    def move(self, event):
        """ Accepts an event and checks if either side arrow key is depressed. Adjusts lateral
        position accordingly."""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.xchange -= 8
            elif event.key == pygame.K_RIGHT:
                self.xchange += 8
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.xchange = 0

        self.rect_type = pygame.Rect(self.xpos, self.ypos, self.width, self.height)

import pygame


""" This file serves as a container for all game assets and
other constants referenced by the game code. Also initializes
images and display surface."""

# Initializes display surface.
aspect_ratio = (800, 600)
game_display = pygame.display.set_mode(aspect_ratio)
pygame.display.set_caption("Chicken Chaser")
clock = pygame.time.Clock()

# Sounds
squish_sound = "squish.wav"
crash_sound = "crash.wav"
game_music = "chicken_dance.wav"

# Images
background = pygame.image.load("cchd.png").convert_alpha()
game_icon = pygame.image.load("chicken_icon.png").convert_alpha()
car_sprite = pygame.image.load("tractor_sprite.png").convert_alpha()
chicken_sprite = pygame.image.load("zelda_chicken.png").convert_alpha()
blood_splatter = pygame.image.load("blood.png").convert_alpha()

# Sets window icon.
pygame.display.set_icon(game_icon)

# Defines several colors for pygame to use.
colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "darkRed": (175, 0, 0),
    "darkGreen": (0, 175, 0)
}

# Defines a list of insults to display in game.
lossList = ["That's what you call driving?", "Your mother was a hamster!",
            "Your father smelt of elderberries!"]

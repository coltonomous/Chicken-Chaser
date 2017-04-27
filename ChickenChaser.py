import pygame
import random

""" This is the source code for a game where you control the lateral movements of a tractor
to avoid chickens. Score is awarded for being on course to hit the chickens without actually hitting them and
is subtracted for hitting and killing chickens. Vehicle movements are controlled with the side arrow keys.
Additionally, the game can be paused by pressing the "p" key. Almost all parts of this game were made by me.
Notable exceptions are the blood splatter which was borrowed from polyvore.com and the chicken art which was made
by my amazing girlfriend. I would also like to specially acknowledge 'sentdex', whose youtube tutorials helped
make this possible."""

########################################################################################################################
############################################# Gamespace Setup ##########################################################
########################################################################################################################

pygame.init()

# Defines all the sounds used in the game.
squish_sound = pygame.mixer.Sound("squish.wav")
crash_sound = pygame.mixer.Sound("crash.wav")
game_music = pygame.mixer.music.load("chicken_dance.wav")

xDisplay = 800
yDisplay = 600

# Defines all game art assets.
gameDisplay = pygame.display.set_mode((xDisplay, yDisplay))
pygame.display.set_caption("Chicken Chaser")
gameIcon = pygame.image.load("chicken_icon.png")
carSprite = pygame.image.load("tractor_sprite.png").convert_alpha()
chickenSprite = pygame.image.load("chicken_sprite.png").convert_alpha()
bloodSplatter = pygame.image.load("blood.png").convert_alpha()
pygame.display.set_icon(gameIcon)

carWidth = int(0.105 * xDisplay)
carHeight = int(0.233 * yDisplay)
carSprite = pygame.transform.scale(carSprite, (carWidth, carHeight))

chickenWidth = int(0.1 * xDisplay)
chickenHeight = int(0.108 * yDisplay)
chickenSprite = pygame.transform.scale(chickenSprite, (chickenWidth, chickenHeight))

bloodWidth = int(0.1875 * xDisplay)
bloodHeight = int(0.25 * yDisplay)
bloodSplatter = pygame.transform.scale(bloodSplatter, (bloodWidth, bloodHeight))

colors = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 0),
          "yellow": (255, 255, 0), "darkRed": (175, 0, 0), "darkGreen": (0, 175, 0),
          "brown": (121, 67, 33), "grey": (125, 125, 125), "darkGrey": (75, 75, 75), "darkYellow": (175, 175, 0)}

lossList = ["That's what you call driving?", "Your mother was a hamster!",
            "Your father smelt of elderberries!"]

lossCount = -1

clock = pygame.time.Clock()


########################################################################################################################
############################################ Game Functions ############################################################
########################################################################################################################

def game_intro():
    """ This function generates the game's start menu. It has a play button and a quit button. It also has a
    chicken_sprite that moves back and forth across the screen."""

    chick_x = xDisplay * 0.1875
    chick_dir = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if chick_x > xDisplay * 0.65:
            chick_dir = False
        elif chick_x < xDisplay * 0.1875:
            chick_dir = True

        if chick_dir:
            chick_x += 5
        else:
            chick_x -= 5

        chick_y = yDisplay * 0.55

        gameDisplay.fill(colors["black"])
        pygame.draw.rect(gameDisplay, colors["brown"], (10, 10, xDisplay - 20, yDisplay - 20))
        message_display(xDisplay / 2, yDisplay / 3, 75, "Chicken! Bwak!")

        chickens(chick_x, chick_y)

        buttons("I'm no chicken!", 0.15 * xDisplay, 0.75 * yDisplay, 175, 50,
                colors["darkGreen"], colors["green"], "play")
        buttons("Chicken out...", 0.65 * xDisplay, 0.75 * yDisplay, 175, 50, colors["darkRed"], colors["red"], "quit")

        pygame.display.update()
        clock.tick(60)


def buttons(message, x, y, width, height, inactive_color, active_color, action):
    """ This function generates a button at (x, y) of width and height. When the mouse is over the button,
    the color changes from inactive_color to active_color. Function is displayed on the button. Clicking
    on the button activates the action."""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, colors["black"], (x, y, width, height))
        pygame.draw.rect(gameDisplay, active_color, (x + 2, y + 2, width - 4, height - 4))

        if click[0] == 1:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, colors["black"], (x, y, width, height))
        pygame.draw.rect(gameDisplay, inactive_color, (x + 2, y + 2, width - 4, height - 4))

    message_display(x + (width / 2), y + (height / 2), 20, message)


def tractor(tractor_x, tractor_y):
    """ This function draws the tractor to the gameDisplay at position (tractor_x, tractor_y)."""
    gameDisplay.blit(carSprite, (tractor_x, tractor_y))


def chickens(obx, oby):
    """ This function draws a chicken to gameDisplay at obx and oby."""
    gameDisplay.blit(chickenSprite, (obx, oby))


def blood_splatter(obx, oby):
    """ Draws blood at coordinates obx and oby."""
    gameDisplay.blit(bloodSplatter, (obx - (chickenWidth / 2), oby - (chickenHeight / 2)))


def message_display(horiz, vert, text_size, text):
    """ This function writes text of text_size to gameDisplay at horiz and vert coordinates."""
    print_text = pygame.font.Font("fixedsys.ttf", text_size)
    text_surface = print_text.render(text, True, colors["black"])
    text_rect = text_surface.get_rect()
    text_rect.center = (horiz, vert)
    gameDisplay.blit(text_surface, text_rect)


def count(game_count, chicken_count):
    """ This function prints the updating score and the number of chickens
     remaining in the game to the gameDisplay. """
    score_text = "Score: " + str(game_count)
    chicken_text = "Remaining: " + str(chicken_count)
    message_display(xDisplay * 0.9, yDisplay * 0.025, 25, score_text)
    message_display(xDisplay * 0.15, yDisplay * 0.025, 25, chicken_text)


def crash():
    """ This function prints to the gameDisplay 'You crashed!' and offers buttons to
     try again or quit."""

    global lossCount

    if lossCount < len(lossList) - 1:
        lossCount += 1
    else:
        lossCount = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        message_display(xDisplay / 2, yDisplay / 3, 30, lossList[lossCount])

        buttons("Play Again?", 0.2125 * xDisplay, 0.75 * yDisplay, 130, 50, colors["darkGreen"],
                colors["green"], "play")
        buttons("Quit", 0.6875 * xDisplay, 0.75 * yDisplay, 100, 50, colors["darkRed"],
                colors["red"], "quit")

        pygame.display.update()
        clock.tick(15)


def paused(pause):
    """ This function pauses and unpauses the game state."""
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    pygame.mixer.music.unpause()

        message_display(xDisplay / 2, yDisplay / 3, 75, "Paused")
        pygame.display.update()
        clock.tick(60)


def win(score, objects):
    """ This function displays stats about a played game, including
    the final score and the average score obtained per chicken. """

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(colors["black"])
        pygame.draw.rect(gameDisplay, colors["brown"], (10, 10, xDisplay - 20, yDisplay - 20))
        message_display(xDisplay / 2, yDisplay / 4, 40, "Winner winner chicken dinner!")
        message_display(xDisplay / 2, yDisplay / 2, 30, "Final score: " + str(score))
        average = round(float(score) / float(objects), 1)
        message_display(xDisplay / 2, 3 * yDisplay / 5, 30, "Average per chicken: " + str(average))

        buttons("Play again?", 0.15 * xDisplay, 0.75 * yDisplay, 175, 50,
                colors["darkGreen"], colors["green"], "play")
        buttons("Chicken out...", 0.65 * xDisplay, 0.75 * yDisplay, 175, 50, colors["darkRed"], colors["red"], "quit")

        pygame.display.update()
        clock.tick(60)


########################################################################################################################
############################################# Main Game Loop ###########################################################
########################################################################################################################

def game_loop():
    # Coordinates for tractor.
    x_pos = xDisplay * 0.455
    y_pos = yDisplay * 0.75
    x_change = 0

    # Coordinates for chicken.
    chicken_speed = 0.00833 * yDisplay
    chicken_x = random.randrange(25, int(xDisplay - (chickenWidth + 25)))
    chicken_y = -yDisplay

    score = 0
    chickenCount = 30
    passed = 0
    hit = False

    pygame.mixer.music.play(-1)

    while chickenCount > 0:

        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -0.01 * xDisplay
                elif event.key == pygame.K_RIGHT:
                    x_change = 0.01 * xDisplay
                elif event.key == pygame.K_p:
                    paused(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x_pos += x_change

        # Handles crashing into boundaries
        if x_pos + carWidth >= xDisplay + 10 or x_pos <= -10:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(crash_sound)
            crash()

        # Handles crashing into chickens
        if y_pos + 0.03 * yDisplay < chicken_y + chickenHeight and \
                (x_pos + (0.03 * xDisplay) < chicken_x < x_pos + carWidth - (0.03 * xDisplay) or
                x_pos + (0.03 * xDisplay) < chicken_x + chickenWidth < x_pos + carWidth - (0.03 * xDisplay) or
                x_pos < chicken_x + (chickenWidth / 2) < x_pos + carWidth) and not hit:
            pygame.mixer.Sound.play(squish_sound)
            hit = True
            if score >= 50:
                score -= 50
            else:
                score = 0

        # Updates score while on path to crash into chickens.
        elif (x_pos + (0.03 * xDisplay) < chicken_x < x_pos + carWidth - (0.03 * xDisplay) or
                x_pos + (0.03 * xDisplay) < chicken_x + chickenWidth < x_pos + carWidth - (0.03 * xDisplay) or
                x_pos < chicken_x + (chickenWidth / 2) < x_pos + carWidth) and not hit:
            score += 1

        # Handles drawing of chickens
        if chicken_y > yDisplay:
            chicken_y = 0 - chickenHeight
            chicken_x = random.randrange(25, int(xDisplay - (chickenWidth + 25)))
            chickenCount -= 1
            passed += 1
            hit = False
            # Updates difficulty
            if chicken_speed < 0.0210 * yDisplay:
                chicken_speed += 0.00075 * yDisplay

        # "Graphic" rendering
        gameDisplay.fill(colors["darkGreen"])
        pygame.draw.rect(gameDisplay, colors["brown"], (25, 0, xDisplay - 50, yDisplay))
        if hit:
            blood_splatter(chicken_x, chicken_y)
        else:
            chickens(chicken_x, chicken_y)
        tractor(x_pos, y_pos)
        chicken_y += chicken_speed
        count(score, chickenCount)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.fadeout(2000)
    win(score, passed)

game_intro()

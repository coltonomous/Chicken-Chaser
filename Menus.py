import Obstacles
from Assets import *


class Menus:

    def __init__(self, action):
        self.action = action


    def activate(self):
        if self.action == "start":
            self.start_menu()
        elif self.action == "pause":
            self.pause_menu()
        elif self.action == "crash":
            self.crash()
        elif self.action == "win":
            self.win()

    def quit_game(event):
        """ Checks each passed event to see if player wants to quit.
        Quits is quit event is passed."""

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    def start_menu(self):
        """ This function generates the game's start menu. It has a play button and a quit button. It also has a
        chicken_sprite that moves back and forth across the screen."""

        chick_x = aspect_ratio[0] * 0.1875
        chick_dir = True

        while 1:
            for event in pygame.event.get():
                self.quit_game(event)

            # Determines lateral movement of chicken and chicken position.
            if chick_x > aspect_ratio[0] * 0.65:
                chick_dir = False
            elif chick_x < aspect_ratio[0] * 0.1875:
                chick_dir = True

            if chick_dir:
                chick_x += 5
            else:
                chick_x -= 5

            chick_y = aspect_ratio[1] * 0.55

            # Draws intro screen to game display.
            game_display.blit(background, (0, 0))
            message_display(aspect_ratio[0] / 2, aspect_ratio[1] / 3, 75, "Chicken! Bwak!")

            chickens(chick_x, chick_y)

            buttons("I'm no chicken!", 0.15 * aspect_ratio[0], 0.75 * aspect_ratio[1], 175, 50,
                    colors["darkGreen"], colors["green"], "play")
            buttons("Chicken out...", 0.65 * aspect_ratio[0], 0.75 * aspect_ratio[1], 175, 50, colors["darkRed"], colors["red"], "quit")

            pygame.display.update()
            clock.tick(60)


    def pause_menu(self):
        """ This function pauses and unpauses the game state."""
        pygame.mixer.music.pause()

        while pause:
            for event in pygame.event.get():
                self.quit_game(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
                        pygame.mixer.music.unpause()

            message_display(aspect_ratio[0] / 2, aspect_ratio[1] / 3, 75, "Paused")
            pygame.display.update()
            clock.tick(15)


    def crash(self):
        """ This function prints assorted insults to the gameDisplay and offers buttons to
         try again or quit."""

        global lossCount

        if lossCount < len(lossList) - 1:
            lossCount += 1
        else:
            lossCount = 0

        while 1:
            for event in pygame.event.get():
                self.quit_game(event)

            message_display(aspect_ratio[0] / 2, aspect_ratio[1] / 3, 30, lossList[lossCount])

            buttons("Play Again?", 0.2125 * aspect_ratio[0], 0.75 * aspect_ratio[1], 130, 50, colors["darkGreen"],
                    colors["green"], "play")
            buttons("Chicken out...", 0.65 * aspect_ratio[0], 0.75 * aspect_ratio[1], 175, 50, colors["darkRed"], colors["red"],
                    "quit")

            pygame.display.update()
            clock.tick(15)


    def win_menu(self):
        """ This function displays stats about a played game, including
        the final score and the average score obtained per chicken. """
        pygame.mixer.music.fadeout(2000)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            message_display(aspect_ratio[0] / 2, aspect_ratio[1] / 4, 40, "Winner winner chicken dinner!")
            message_display(aspect_ratio[0] / 2, aspect_ratio[1] / 2, 30, "Final score: " + str(score))
            average = round(float(score) / float(objects), 1)
            message_display(aspect_ratio[0] / 2, 3 * aspect_ratio[1] / 5, 30, "Average per chicken: " + str(average))

            buttons("Play again?", 0.15 * aspect_ratio[0], 0.75 * aspect_ratio[1], 175, 50,
                    colors["darkGreen"], colors["green"], "play")
            buttons("Chicken out...", 0.65 * aspect_ratio[0], 0.75 * aspect_ratio[1], 175, 50, colors["darkRed"], colors["red"], "quit")

            pygame.display.update()
            clock.tick(15)

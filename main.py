import pygame

pygame.init()

#CONSTANTS
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500

class Game:
    def __init__(self):
        self.game_window = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )

        self.game_running = True

    def main_loop(self):
        while self.game_running:
            self.__handle_events()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False

if __name__ == "__main__":
    game = Game()
    game.main_loop()
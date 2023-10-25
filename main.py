import pygame

pygame.init()

#CONSTANTS
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
BACKGROUND_COLOR = ( 145, 245, 95 )

FPS = 60

ROAD_MARGIN = 50
ROAD_COLOR = (130, 128, 122)

CAR_WIDTH = 35
CAR_HEIGHT = 50
PLAYER_CAR_POSITION = ( (WINDOW_WIDTH - CAR_WIDTH )//2, (WINDOW_HEIGHT - 50 - CAR_HEIGHT//2) )
PLAYER_COLOR = ( 255,0,0 )

class Game:
    def __init__(self):
        self.game_window = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
        pygame.display.set_caption( "Car Game" )

        self.game_running = True
        self.clock = pygame.time.Clock()

        self.road = Road()
        self.player_car = Car(color= PLAYER_COLOR)

    def main_loop(self):
        while self.game_running:
            self.__handle_events()
            self.__clear_screen()
            self.__draw_screen()
            self.__update_screen()
            self.clock.tick(FPS)

    def __handle_events(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.player_car.move_left()
        elif pressed_keys[pygame.K_RIGHT]:
            self.player_car.move_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
    
    def __draw_screen(self):
        self.road.draw(self.game_window)
        self.player_car.draw(self.game_window)

    def __clear_screen(self):
        self.game_window.fill( BACKGROUND_COLOR )

    def __update_screen(self):
        pygame.display.update()

class Road:
    def __init__(self):
        self.road_width = WINDOW_WIDTH - 2*ROAD_MARGIN
        self.road_height = WINDOW_HEIGHT
        self.left = ROAD_MARGIN
        self.top = 0

    def draw(self, surface : pygame.Surface):
        pygame.draw.rect(surface, ROAD_COLOR, [self.left, self.top, self.road_width, self.road_height])

class Car(pygame.Rect):
    def __init__(self, center = None, color = None):
        self.center = center if center else PLAYER_CAR_POSITION
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = color

    def draw(self, surface : pygame.Surface):
        pygame.draw.rect(surface, self.color, self)

    def move_left(self):
        if self.left <= ROAD_MARGIN:
            self.left = ROAD_MARGIN
            return
        self.left -= 10
    def move_right(self):
        if self.right >= WINDOW_WIDTH - ROAD_MARGIN:
            self.right = WINDOW_WIDTH - ROAD_MARGIN
            return
        self.right += 10
        

    


if __name__ == "__main__":
    game = Game()
    game.main_loop()
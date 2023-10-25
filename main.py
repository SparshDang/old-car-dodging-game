import pygame
import random

pygame.init()

# CONSTANTS
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
BACKGROUND_COLOR = (145, 245, 95)

FPS = 60

CAR_WIDTH = 35
CAR_HEIGHT = 50
PLAYER_CAR_POSITION = ((WINDOW_WIDTH - CAR_WIDTH)//2,
                       (WINDOW_HEIGHT - 50 - CAR_HEIGHT//2))
PLAYER_COLOR = (255, 0, 0)
NPC_COLORS = ((255, 255, 0), (0, 255, 0), (0, 0, 255))
TEXT_COLOR = (255,0,0)

ROAD_MARGIN = 50
ROAD_WIDTH = WINDOW_WIDTH - 2*ROAD_MARGIN
ROAD_COLOR = (130, 128, 122)
ROAD_SEGMENTS = ROAD_WIDTH // CAR_WIDTH 

CAR_TOP_SPEED = 10


class Game:
    def __init__(self):
        self.game_window = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Car Game")

        self.game_running = True
        self.game_over = False
        self.game_start = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 55)

        self.road = Road()
        self.player_car = Car(color=PLAYER_COLOR)
        self.npc_cars = []
        self.cars_dodged = 0

        self.__init_npc_cars()

    def __init_npc_cars(self):
        for _ in range(6):
            while True:
                correct = True
                car = Car.create_npc_car(True)
                for car_ in self.npc_cars:
                    if car.left in range(car_.left - CAR_WIDTH, car_.right) and car.top in range(car_.top - CAR_HEIGHT, car_.bottom):
                        correct = False
                        break
                if correct:
                    break

            self.npc_cars.append(car)

    def main_loop(self):
        while self.game_running:
            self.__handle_events()
            if not self.game_over:
                self.__clear_screen()
                self.__draw_screen()
                if self.game_start:
                    self.__update_npc_cars()
                self.__check_collisions()
            
            if not self.game_start or self.game_over:
                self.__show_front_screen()
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__reset()
                    else:
                        self.game_start = True


    def __draw_screen(self):
        self.road.draw(self.game_window)
        self.player_car.draw(self.game_window)
        self.__draw_npc_cars()
        self.__show_score()

    def __show_front_screen(self):
        text = self.font.render( "Press Spacebar", True, TEXT_COLOR)
        text_rect = text.get_rect()
        coords = ( (WINDOW_WIDTH - text_rect.width)//2, (WINDOW_HEIGHT - text_rect.height)//2  )
        self.game_window.blit( text, coords)
        

    def __draw_npc_cars(self):
        for car in self.npc_cars:
            car.draw(self.game_window)
    
    def __update_npc_cars(self):
        for index, cars in enumerate(self.npc_cars):
            cars.update_y()
            if cars.get_top() > WINDOW_HEIGHT:
                del cars
                self.npc_cars[index] = Car.create_npc_car()
                self.cars_dodged +=1
                Car.car_speed = min(5 + self.cars_dodged//10, CAR_TOP_SPEED)

    def __show_score(self):
        text = self.font.render(f"Cars Dodged : {self.cars_dodged}", True, TEXT_COLOR )
        self.game_window.blit(text, (0,0))

    def __check_collisions(self):
        if self.player_car.collideobjects(self.npc_cars):
            self.game_over = True

    def __clear_screen(self):
        self.game_window.fill(BACKGROUND_COLOR)

    def __update_screen(self):
        pygame.display.update()

    def __reset(self):
        self.game_over = False
        self.game_start = False
        Car.car_speed = 5

        self.player_car = Car(color=PLAYER_COLOR)
        self.npc_cars = []
        self.cars_dodged = 0

        self.__init_npc_cars()



class Road:
    def __init__(self):
        self.road_width = WINDOW_WIDTH - 2*ROAD_MARGIN
        self.road_height = WINDOW_HEIGHT
        self.left = ROAD_MARGIN
        self.top = 0

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, ROAD_COLOR, [
                         self.left, self.top, self.road_width, self.road_height])


class Car(pygame.Rect):
    car_speed = 5
    def __init__(self, center=None, color=None):
        self.center = center if center else PLAYER_CAR_POSITION
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = color

    def draw(self, surface: pygame.Surface):
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

    @classmethod
    def create_npc_car(cls, random_top=False):
        car_left = random.choice(range(ROAD_SEGMENTS)) * CAR_WIDTH + ROAD_MARGIN
        car_top = -CAR_HEIGHT
        if random_top:
            car_top = random.randint(-CAR_HEIGHT, int(WINDOW_HEIGHT * (3/4)))
        car_color = random.choice(NPC_COLORS)

        return cls(center=(car_left + CAR_WIDTH//2, car_top), color=car_color)
    
    def update_y(self):
        self.top += self.car_speed

    def get_top(self):
        return self.top


if __name__ == "__main__":
    game = Game()
    game.main_loop()

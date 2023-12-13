import pygame
from pygame.locals import *
import random
# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)


# window properties
width = 500
height = 500
screen_size = (width, height)

# road and marker sizes
road_width = 300
marker_width = 10
marker_height = 50

# lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# player's starting coordinates
player_x = 250
player_y = 400

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

class Game:
    def __init__(self):
        pygame.init()
        self.screen_size = (screen_size)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Car Game')
        self.clock = pygame.time.Clock()
        self.fps = 120
        self.gameover = False
        self.speed = 2
        self.score = 0
        self.player = PlayerVehicle(player_x, player_y)
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.vehicle_group = pygame.sprite.Group()
        self.vehicle_images = []
        self.crash = pygame.image.load('images/crash.png')
        self.crash_rect = self.crash.get_rect()
        # load the vehicle images
        image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
        self.vehicle_images = []
        for image_filename in image_filenames:
            image = pygame.image.load('images/' + image_filename)
            self.vehicle_images.append(image)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.gameover = True
            if event.type == KEYDOWN:
                if event.key == K_LEFT and self.player.rect.center[0] > left_lane:
                    self.player.rect.x -= 100
                elif event.key == K_RIGHT and self.player.rect.center[0] < right_lane:
                    self.player.rect.x += 100

    def update_game_state(self):
        for vehicle in self.vehicle_group:
            vehicle.rect.y += self.speed
            if vehicle.rect.top >= self.screen_size[1]:
                vehicle.kill()
                self.score += 1
                if self.score > 0 and self.score % 5 == 0:
                    self.speed += 1

        if pygame.sprite.spritecollide(self.player, self.vehicle_group, True):
            self.gameover = True
            self.crash_rect.center = [self.player.rect.center[0], self.player.rect.top]

    def render_game(self):
        self.screen.fill(green)
        pygame.draw.rect(self.screen, gray, road)
        pygame.draw.rect(self.screen, yellow, left_edge_marker)
        pygame.draw.rect(self.screen, yellow, right_edge_marker)
        
        lane_marker_move_y = 0
        lane_marker_move_y += self.speed * 2

        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, height, marker_height * 2):
            
            pygame.draw.rect(self.screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(self.screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        self.player_group.draw(self.screen)
        
        if len(self.vehicle_group) < 2:
        
            add_vehicle = True
            for vehicle in self.vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
                
            if add_vehicle:
            
                # select a random lane
                lane = random.choice(lanes)
            
                # select a random vehicle image
                image = random.choice(self.vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                self.vehicle_group.add(vehicle)
        
        self.vehicle_group.draw(self.screen)
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Score: ' + str(self.score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 400)
        self.screen.blit(text, text_rect)
        if self.gameover:
            self.screen.blit(self.crash, self.crash_rect)
            pygame.draw.rect(self.screen, red, (0, 50, width, 100))
            text = font.render('Game over. Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            self.screen.blit(text, text_rect)
        pygame.display.update()

    def run(self):
        while not self.gameover:
            self.handle_events()
            self.update_game_state()
            self.render_game()
            self.clock.tick(self.fps)

        while self.gameover:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.gameover = False
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        self.gameover = False
                        self.speed = 2
                        self.score = 0
                        self.vehicle_group.empty()
                        self.player.rect.center = [player_x, player_y]
                    elif event.key == K_n:
                        self.gameover = False

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
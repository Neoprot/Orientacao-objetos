import time
import pygame
from pygame.locals import *
from utils import draw_car, move_player, scale_image, blit_text_center
from models.Vehicle import Scootermoto, Custommoto, Sportmoto, BotVehicle
from models.Camera import CameraGroup
from models.Button import Button
import random

TRACK = pygame.image.load("images/lvl1.png")
MENU = pygame.image.load("images/menu.jpeg")

# screen size
SCREE_SIZE = (600, 800)

# colors
GREEN = (76, 208, 56)
RED = (200, 0, 0)

# window properties

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, 800))

# player's starting coordinates
player_x = 100
player_y = HEIGHT - 100


class GameInfo:
    # LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    # def next_level(self):
    #     self.level += 1
    #     self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    # def game_finished(self):
    #     return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        return 0 if not self.started else round(time.time() - self.level_start_time)


class Game():
    def __init__(self):
        pygame.init()
        self.screen_size = SCREE_SIZE
        self.camera_group = CameraGroup()
        self.main_font = pygame.font.SysFont("comicsans", 44)
        self.screen_size = (600, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("ROAD RASH")
        self.clock = pygame.time.Clock()
        self.fps = 120
        self.level_clear = False
        self.running = True
        self.vehicle_images = []
        self.images = [(TRACK, (0, 0))]
        self.final_position = 0

        # load the vehicle images
        image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png', 'moto2.png']
        self.vehicle_images = []
        for image_filename in image_filenames:
            image = pygame.image.load(f'images/{image_filename}')
            self.vehicle_images.append(image)

        self.bot_vehicles = []
        for _ in range(5):
            random_offset = random.randint(50, 450)
            bot = BotVehicle(self.vehicle_images[4], player_x + random_offset, player_y, self.camera_group)
            self.bot_vehicles.append(bot)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and self.level_clear:
                self.running = False

        self.keys = pygame.key.get_pressed()
        if self.player.bounce():
            self.player.vel = -self.player.vel
        move_player(self.player, self.keys)

    def draw_win_message(self, window):
        if self.player.y < 50:
            positions = self.get_vehicle_positions()
            for i, (x, y, t) in enumerate(positions):
                if t == type(self.player) and self.final_position == 0 :
                    self.final_position = i + 1
                    self.write_data(self.final_position)
            self.level_clear = True
            win_font = pygame.font.SysFont("comicsans", 70)
            win_text = win_font.render("YOU WIN!", 1, (0, 0, 0))
            window.blit(MENU, (0, 0))
            window.blit(win_text, (WIDTH / 3 - win_text.get_width() / 3, 300 - win_text.get_height() / 2))
            blit_text_center(WIN, self.main_font, "Press any key to close")

    def moto_menu(self, window):
        moto1_button = Button(GREEN, 50, 200, 200, 100, 'Sport')
        moto2_button = Button(GREEN, 300, 200, 200, 100, 'Custom')
        moto3_button = Button(GREEN, 200, 350, 200, 100, 'Scooter')
        win_font = pygame.font.SysFont("comicsans", 60)
        win_text = win_font.render("Escolha sua moto", 1, (0, 0, 0))

        run = True
        while run:
            window.blit(MENU, (0, 0))
            window.blit(win_text, (WIDTH / 2.5 - win_text.get_width() / 3, 100 - win_text.get_height() / 2))
            moto1_button.draw(self.screen)
            moto2_button.draw(self.screen)
            moto3_button.draw(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if moto1_button.is_over(pos):
                        game_info.started = True
                        run = False
                        self.player = Sportmoto(player_x, player_y, self.camera_group)
                    elif moto2_button.is_over(pos):
                        game_info.started = True
                        run = False
                        self.player = Custommoto(player_x, player_y, self.camera_group)
                    elif moto3_button.is_over(pos):
                        game_info.started = True
                        run = False
                        self.player = Scootermoto(player_x, player_y, self.camera_group)

    def start_menu(self, window):
        start_button = Button(GREEN, 200, 200, 200, 100, 'Start')
        history_button = Button(GREEN, 200, 400, 200, 100, 'History')
        win_font = pygame.font.SysFont("comicsans", 70)
        win_text = win_font.render("ROAD RASH", 1, (0, 0, 0))

        run = True
        while run:
            window.blit(MENU, (0, 0))
            window.blit(win_text, (WIDTH / 2.5 - win_text.get_width() / 3, 100 - win_text.get_height() / 2))
            start_button.draw(self.screen)
            history_button.draw(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_over(pos):
                        run = False
                        self.moto_menu(self.screen)
                    if history_button.is_over(pos):
                        print('Clicked the history button')
                        # Here you can add the code to show the history

    def get_vehicle_positions(self):
        # Create a list of tuples containing vehicle and its y-coordinate
        positions = [(self.player.x, self.player.y, type(self.player))]
        positions.extend([(bot.x, bot.y, type(bot)) for bot in self.bot_vehicles])

        # Sort the list based on y-coordinate in descending order
        positions.sort(key=lambda x: x[1])

        return positions

    def render_game(self):
        if not self.level_clear:

            # Draw the player
            self.camera_group.box_target_camera(self.player)

            bot_images = [(bot.image, (bot.x, bot.y)) for bot in self.bot_vehicles]
            all_images = self.images + bot_images

            draw_car(self.screen, self.player, all_images, self.camera_group.offset)

            # Draw the bot
            for bot in self.bot_vehicles:
                bot.update_ai()

            if self.keys[K_w]:
                pygame.draw.rect(self.screen, RED, self.player.punch())
            elif self.keys[K_s]:
                pygame.draw.rect(self.screen, RED, self.player.kick())

        pygame.display.update()

    def run(self):
        while self.running:

            while not game_info.started:
                self.start_menu(self.screen)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        break

            self.handle_events()
            self.render_game()
            self.draw_win_message(self.screen)
            self.clock.tick(self.fps)
        pygame.quit()

    def write_data(self, r):
        with open('data/history.txt', 'a') as archive:
            archive.write(str(r) + '\n')


game_info = GameInfo()
g = Game()
g.run()

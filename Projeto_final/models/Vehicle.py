import pygame
import math
from utils import blit_rotate_center

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y, max_vel, rotation_vel, acceleration, group=None):
        super().__init__(group)
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.center = [x, y]
        self.x = x
        self.y = y

        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.acceleration = acceleration

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

        self.update_rect_position(-horizontal, -vertical)

    def bounce(self):
        return self.x < 25 or self.x > 540

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen, camera_offset):
        blit_rotate_center(screen, self.image, (self.x - camera_offset.x, self.y - camera_offset.y), self.angle)

    def update_rect_position(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y


class PlayerVehicle(Vehicle):
    def __init__(self, image,x, y, max_vel, rotation_vel, acceleration, group):
        super().__init__(image, x, y, max_vel, rotation_vel, acceleration, group)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def punch(self):
        return (self.x + 20, self.y, 35, 20)

    def kick(self):
        return (self.x - 20, self.y, 35, 20)

class BotVehicle(Vehicle):
    def __init__(self, image, x, y, group=None):
        max_vel = 5
        rotation_vel = 1
        acceleration = 0.05
        super().__init__(image, x, y, max_vel, rotation_vel, acceleration, group)

class Scootermoto(PlayerVehicle):
    def __init__(self, x, y, group):
        image = pygame.image.load('images/moto1.png').convert_alpha()
        acceleration = 0.05
        max_vel = 6
        rotation_vel = 2
        super().__init__(image, x, y, max_vel, rotation_vel, acceleration, group)

class Sportmoto(PlayerVehicle):
    def __init__(self, x, y, group):
        image = pygame.image.load('images/moto2.png').convert_alpha()
        acceleration = 0.07
        max_vel = 7
        rotation_vel = 0.5
        super().__init__(image, x, y, max_vel, rotation_vel, acceleration, group)
        
class Custommoto(PlayerVehicle):
    def __init__(self, x, y, group):
        image = pygame.image.load('images/moto3.png').convert_alpha()
        acceleration = 0.1
        max_vel = 5
        rotation_vel = 1
        super().__init__(image, x, y, max_vel, rotation_vel, acceleration, group)

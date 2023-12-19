import pygame

TRACK = pygame.image.load("images/lvl1.png")
MENU = pygame.image.load("images/menu.jpeg")

SCREE_SIZE = (600, 800)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, 800))

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = SCREE_SIZE[0] // 2
        self.half_h = SCREE_SIZE[1] // 2

        # box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = SCREE_SIZE[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = SCREE_SIZE[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):
        camera_height = 800
        
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

        if self.offset.x < 0 or self.offset.x > 0:
            self.offset.x = 0
        if self.offset.y < 0:
            self.offset.y = 0
        elif self.offset.y > HEIGHT - camera_height :
            self.offset.y = HEIGHT - camera_height
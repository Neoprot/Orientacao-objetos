import pygame

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        radius = 20
        pygame.draw.rect(win, self.color, (self.x, self.y + radius, self.width, self.height - 2*radius))
        pygame.draw.rect(win, self.color, (self.x + radius, self.y, self.width - 2*radius, self.height))
        pygame.draw.circle(win, self.color, (self.x + radius, self.y + radius), radius)
        pygame.draw.circle(win, self.color, (self.x + self.width - radius, self.y + radius), radius)
        pygame.draw.circle(win, self.color, (self.x + radius, self.y + self.height - radius), radius)
        pygame.draw.circle(win, self.color, (self.x + self.width - radius, self.y + self.height - radius), radius)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

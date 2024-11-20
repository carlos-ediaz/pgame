import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #self.color = self.settings.bullet_color
        #self.rect =pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        #self.rect.midtop = ai_game.ship.rect.midtop
        self.image = pygame.image.load('images/bullet.bmp')
        self.image = pygame.transform.scale(self.image, (18, 54))
        self.rect = self.image.get_rect()

        self.rect.midtop = ai_game.ship.rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    #def draw_bullet(self):
    #    pygame.draw.rect(self.screen, self.rect)
    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)

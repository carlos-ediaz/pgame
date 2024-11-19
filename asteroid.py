import random
import pygame
from pygame.sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/asteroid.bmp')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.rect.x = random.choice([0, self.settings.screen_width])
        self.rect.y = random.choice([0, self.settings.screen_height])

        self.direction_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.direction_y = random.choice([-1, 1]) * random.uniform(0.5, 1.5)

        self.speed = random.uniform(1, 3)
    
    def update(self):
        """Mover el asteroide."""
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Eliminar el asteroide si sale de la pantalla
        if (self.rect.right < 0 or self.rect.left > self.settings.screen_width or self.rect.bottom < 0 or self.rect.top > self.settings.screen_height):
            self.kill()
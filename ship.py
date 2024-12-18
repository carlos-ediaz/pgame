import pygame
#from pygame.sprite import Sprite

class Ship():
    def __init__(self, ai_game):

        #super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')

        #change ship size
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #self.rect.center = self.screen_rect.center


        #Decimal value for the ship's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

import os
import sys
import random
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Obtener una imagen aleatoria desde la carpeta
        self.image = self._get_random_image('images/aliens')  # Carpeta con las imágenes
        self.rect = self.image.get_rect()

        # Posición inicial en la esquina superior izquierda
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Posición flotante para movimiento suave
        self.x = float(self.rect.x)
    
    def _get_random_image(self, folder_path):
        """Selecciona una imagen aleatoria de una carpeta."""
        # Listar todos los archivos en la carpeta
        try:
            images = [file for file in os.listdir(folder_path) if file.endswith(('.bmp'))]
            if not images:
                raise FileNotFoundError("No hay imágenes válidas en la carpeta.")
            
            # Seleccionar una imagen aleatoria
            image_path = os.path.join(folder_path, random.choice(images))
            image = pygame.image.load(image_path)
            
            image = pygame.transform.scale(image, (80, 80))
            return image
        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            sys.exit()
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

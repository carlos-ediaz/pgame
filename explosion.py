import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__(self, ai_game, position):
        super().__init__()
        self.screen = ai_game.screen
        self.frames = []
        self.load_frames('images/exp/')
        self.current_frame = 0
        self.image = self.frames[self.current_frame]  # Primer cuadro de la animación
        self.rect = self.image.get_rect(center=position)
        self.last_update = pygame.time.get_ticks()  # Tiempo del último cambio de cuadro
        self.frame_rate = 50  # Milisegundos entre cuadros

    def load_frames(self, path):
        """Cargar las imágenes de la secuencia de explosión."""
        for file_name in sorted(os.listdir(path)):
            if file_name.endswith('.png'):
                full_path = os.path.join(path, file_name)
                image = pygame.image.load(full_path).convert_alpha()
                self.frames.append(image)

    def update(self):
        now = pygame.time.get_ticks()  # Tiempo actual
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
            else:
                self.kill()  # Eliminar la explosión cuando termine la animación

import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Propiedades del botón principal
        self.width, self.height = 200, 200
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.button_color = (0, 180, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Preparar el mensaje
        self._prep_msg(msg)
    
    def _draw_rounded_button(self, text, center, width, height, color):
        """Dibujar un botón rectangular redondeado dentro del botón principal."""
        rect = pygame.Rect(0, 0, width, height)
        rect.center = center

        # Dibujar rectángulo redondeado
        pygame.draw.rect(self.screen, color, rect, border_radius=15)

    def _draw_triangle_button(self, center, size, color):
        """Dibujar un triángulo dentro del botón principal."""
        x, y = center
        points = [
            (x - size //2 , y - 2*size),
            (x - size //2, y ),
            (x + size, y-size)
        ]

        # Dibujar triángulo
        pygame.draw.polygon(self.screen, color, points)
    
    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Dibujar fondo del botón
        pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=20)

        self._draw_triangle_button((self.rect.centerx, self.rect.bottom - 60), 40, (0, 0, 0))
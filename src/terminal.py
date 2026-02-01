import pygame
import math
from src.settings import (
    TERMINAL_SIZE,
    COLOR_TERMINAL,
    INTERACTION_DISTANCE,
    COLOR_TEXTO,
)


class Terminal:
    def __init__(self, x, y, task_id):
        self.image = pygame.Surface((TERMINAL_SIZE, TERMINAL_SIZE))
        self.image.fill(COLOR_TERMINAL)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.task_id = task_id  # Identificador del puzzle que contiene
        self.active = False  # ¿Está el jugador interactuando ahora?

    def is_player_near(self, player_rect):
        # Calculamos la distancia entre el centro del jugador y la terminal
        dist = math.hypot(
            self.rect.centerx - player_rect.centerx,
            self.rect.centery - player_rect.centery,
        )
        return dist < INTERACTION_DISTANCE

    def draw(self, surface, player_rect):
        surface.blit(self.image, self.rect)

        # Si el jugador está cerca, dibujar un "indicador" de interacción
        if self.is_player_near(player_rect):
            font = pygame.font.SysFont(None, 24)
            img = font.render("Presiona [E] para programar", True, COLOR_TEXTO)
            surface.blit(img, (self.rect.x - 20, self.rect.y - 30))

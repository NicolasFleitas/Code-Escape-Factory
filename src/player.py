import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_PLAYER,
    PLAYER_SPEED,
    PLAYER_SIZE,
)


class Player:
    def __init__(self):
        # Crear un cuadrado para representar al personaje
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect()

        # Posición inicial (centro de la pantalla)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        # Detectar teclas presionadas
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Limitar movimiento a los bordes de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

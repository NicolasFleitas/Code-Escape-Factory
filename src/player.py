import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_PLAYER,
    PLAYER_SPEED,
    PLAYER_SIZE,
)


class Player:
    def __init__(self, x=None, y=None):
        # Crear un cuadrado para representar al personaje
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(COLOR_PLAYER)
        self.rect = self.image.get_rect()

        # Posición inicial
        if x is not None and y is not None:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, walls=[]):
        # Detectar teclas presionadas
        keys = pygame.key.get_pressed()
        old_pos = self.rect.copy()

        # Movimiento Horizontal
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        
        # Colisión Horizontal
        for wall in walls:
            if self.rect.colliderect(wall):
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.rect.left = wall.right
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.rect.right = wall.left

        # Movimiento Vertical
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            
        # Colisión Vertical
        for wall in walls:
            if self.rect.colliderect(wall):
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.rect.top = wall.bottom
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.rect.bottom = wall.top

        # Limitar movimiento a los bordes de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

import pygame
import os
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_PLAYER,
    PLAYER_SPEED,
    PLAYER_SIZE,
)

class Player:
    def __init__(self, x=None, y=None):
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        
        # Posición inicial
        if x is not None and y is not None:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Cargar Sprites
        self.sprites = {}
        self.load_sprites()
        
        # Dirección actual ("frente", "espalda", "izquierda", "derecha")
        self.direction = "frente"
        self.image = self.sprites.get(self.direction)

    def load_sprites(self):
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_player = os.path.join(ruta_base, "assets", "player")
        
        try:
            # Cargar imágenes originales
            frente = pygame.image.load(os.path.join(ruta_player, "frente.png")).convert_alpha()
            espalda = pygame.image.load(os.path.join(ruta_player, "espalda.png")).convert_alpha()
            perfil = pygame.image.load(os.path.join(ruta_player, "perfil.png")).convert_alpha()
            
            # Escalar al tamaño definido en settings
            self.sprites["frente"] = pygame.transform.scale(frente, (PLAYER_SIZE, PLAYER_SIZE))
            self.sprites["espalda"] = pygame.transform.scale(espalda, (PLAYER_SIZE, PLAYER_SIZE))
            self.sprites["derecha"] = pygame.transform.scale(perfil, (PLAYER_SIZE, PLAYER_SIZE))
            # Invertir perfil para la izquierda
            self.sprites["izquierda"] = pygame.transform.flip(self.sprites["derecha"], True, False)
            
        except Exception as e:
            print(f"⚠️ Error cargando sprites del jugador: {e}")
            # Fallback a un color sólido si fallan las imágenes
            surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            surface.fill(COLOR_PLAYER)
            self.sprites = {"frente": surface, "espalda": surface, "izquierda": surface, "derecha": surface}

    def update(self, walls=[]):
        keys = pygame.key.get_pressed()
        
        # Movimiento Horizontal
        moved_h = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.direction = "izquierda"
            moved_h = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.direction = "derecha"
            moved_h = True
        
        # Colisión Horizontal
        for wall in walls:
            if self.rect.colliderect(wall):
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.rect.left = wall.right
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.rect.right = wall.left

        # Movimiento Vertical
        moved_v = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
            if not moved_h: self.direction = "espalda"
            moved_v = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            if not moved_h: self.direction = "frente"
            moved_v = True
            
        # Colisión Vertical
        for wall in walls:
            if self.rect.colliderect(wall):
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.rect.top = wall.bottom
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.rect.bottom = wall.top

        # Actualizar imagen según dirección
        self.image = self.sprites.get(self.direction, self.sprites["frente"])

        # Limitar movimiento a los bordes de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            # Fallback visual
            pygame.draw.rect(surface, (0, 255, 0), self.rect)

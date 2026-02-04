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

        # Dirección actual ("frente", "espalda", "izquierda", "derecha")
        self.direction = "frente"

        # Cargar Sprites (por defecto obrero 1)
        self.sprites = {}
        self.load_sprites(character_id=1)
        
        # Sprite personalizado (si se selecciona uno diferente al default)
        self.custom_sprite = None


    def load_sprites(self, character_id=1):
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_personajes = os.path.join(ruta_base, "assets", "personajes")
        
        try:
            # Construir nombres de archivos basados en el character_id
            archivo_frente = f"obrero{character_id}-frente.png"
            archivo_espalda = f"obrero{character_id}-espalda.png"
            archivo_perfil = f"obrero{character_id}-perfil.png"

            # Cargar imágenes originales
            frente = pygame.image.load(os.path.join(ruta_personajes, archivo_frente)).convert_alpha()
            espalda = pygame.image.load(os.path.join(ruta_personajes, archivo_espalda)).convert_alpha()
            perfil = pygame.image.load(os.path.join(ruta_personajes, archivo_perfil)).convert_alpha()
            
            # Escalar al tamaño definido en settings
            self.sprites["frente"] = pygame.transform.scale(frente, (PLAYER_SIZE, PLAYER_SIZE))
            self.sprites["espalda"] = pygame.transform.scale(espalda, (PLAYER_SIZE, PLAYER_SIZE))
            self.sprites["derecha"] = pygame.transform.scale(perfil, (PLAYER_SIZE, PLAYER_SIZE))
            # Invertir perfil para la izquierda
            self.sprites["izquierda"] = pygame.transform.flip(self.sprites["derecha"], True, False)
            
            # Actualizar imagen actual
            self.image = self.sprites.get(self.direction, self.sprites["frente"])
            
        except Exception as e:
            print(f"⚠️ Error cargando sprites del jugador (obrero {character_id}): {e}")
            # Fallback a un color sólido si fallan las imágenes
            surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            surface.fill(COLOR_PLAYER)
            self.sprites = {"frente": surface, "espalda": surface, "izquierda": surface, "derecha": surface}
            self.image = surface
            
    def set_custom_sprite(self, image):
        """Establece un sprite personalizado único para todas las direcciones (o base)"""
        if image:
            # Escalar al tamaño correcto si es necesario
            if image.get_size() != (PLAYER_SIZE, PLAYER_SIZE):
                image = pygame.transform.scale(image, (PLAYER_SIZE, PLAYER_SIZE))
            
            self.custom_sprite = image
            # Actualizamos direcciones básicas con este sprite
            self.sprites["frente"] = image
            self.sprites["espalda"] = image
            self.sprites["derecha"] = image
            self.sprites["izquierda"] = pygame.transform.flip(image, True, False)
            self.image = image

    def update(self, walls=[]):
        keys = pygame.key.get_pressed()
        
        # 1. MOVER HORIZONTALMENTE
        dx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
            self.direction = "izquierda"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED
            self.direction = "derecha"
            
        self.rect.x += dx
        
        # Colisión Horizontal: Si colisionamos, volvemos atrás
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0: # Íbamos a la derecha
                    self.rect.right = wall.left
                if dx < 0: # Íbamos a la izquierda
                    self.rect.left = wall.right

        # 2. MOVER VERTICALMENTE
        dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= PLAYER_SPEED
            # Priorizamos dirección lateral si ya se está moviendo horizontalmente
            if dx == 0: self.direction = "espalda"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += PLAYER_SPEED
            if dx == 0: self.direction = "frente"
            
        self.rect.y += dy
        
        # Colisión Vertical: Si colisionamos, volvemos atrás
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0: # Íbamos hacia abajo
                    self.rect.bottom = wall.top
                if dy < 0: # Íbamos hacia arriba
                    self.rect.top = wall.bottom

        # 3. ACTUALIZAR IMAGEN
        self.image = self.sprites.get(self.direction, self.sprites["frente"])

        # 4. LIMITAR A LA PANTALLA
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            # Fallback visual
            pygame.draw.rect(surface, (0, 255, 0), self.rect)

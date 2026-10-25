import math

import pygame

from src.asset_paths import asset_path
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_PLAYER,
    PLAYER_SPEED,
    PLAYER_SIZE,
)

# Largest movement applied in one step. A long frame is split into several
# steps so the player cannot skip over a wall between two frames.
MAX_MOVE_STEP = PLAYER_SIZE / 2


def _substeps(distance):
    """Split a movement step so a long frame cannot skip over a thin wall."""
    steps = max(1, math.ceil(abs(distance) / MAX_MOVE_STEP))
    return [distance / steps] * steps

class Player:
    def __init__(self, x=None, y=None):
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        
        # Posición inicial
        if x is not None and y is not None:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Float position: movement is fractional, the rect only mirrors it.
        self._position = pygame.Vector2(self.rect.topleft)

        # Dirección actual ("frente", "espalda", "izquierda", "derecha")
        self.direction = "frente"

        # Cargar Sprites (por defecto obrero 1)
        self.sprites = {}
        self.load_sprites(character_id=1)

    def load_sprites(self, character_id=1):
        try:
            # Construir nombres de archivos basados en el character_id
            archivo_frente = f"obrero{character_id}-frente.png"
            archivo_espalda = f"obrero{character_id}-espalda.png"
            archivo_perfil = f"obrero{character_id}-perfil.png"

            # Cargar imágenes originales
            frente = pygame.image.load(asset_path("personajes", archivo_frente)).convert_alpha()
            espalda = pygame.image.load(asset_path("personajes", archivo_espalda)).convert_alpha()
            perfil = pygame.image.load(asset_path("personajes", archivo_perfil)).convert_alpha()
            
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

    def update(self, dt, direction=(0, 0), walls=()):
        """Move the player for ``dt`` seconds toward ``direction``.

        ``direction`` is an (x, y) vector produced by the input adapter: the
        player never reads the keyboard (CONTRIBUTING section 6). Speed is in
        pixels per second, so movement does not depend on the frame rate.
        """
        move = pygame.Vector2(direction)
        if move.length_squared() > 1:
            # Normalize diagonals: moving two axes at once is not faster.
            move = move.normalize()

        for dx in _substeps(move.x * PLAYER_SPEED * dt):
            self._move_horizontally(dx, walls)
        for dy in _substeps(move.y * PLAYER_SPEED * dt):
            self._move_vertically(dy, walls)
        # Horizontal input wins the facing, as before.
        if move.x < 0:
            self.direction = "izquierda"
        elif move.x > 0:
            self.direction = "derecha"
        elif move.y < 0:
            self.direction = "espalda"
        elif move.y > 0:
            self.direction = "frente"

        self.image = self.sprites.get(self.direction, self.sprites.get("frente"))

        # 4. LIMITAR A LA PANTALLA
        bounds = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        before_clamp = self.rect.topleft
        self.rect.clamp_ip(bounds)
        if self.rect.topleft != before_clamp:
            # The clamp moved the rect: realign instead of keeping the offset.
            self._sync_position()

    def block_left_of(self, blocker):
        """Snap the player flush against the left edge of ``blocker``."""
        self.rect.right = blocker.left
        self._sync_position()

    def _move_horizontally(self, dx, walls):
        self._position.x += dx
        self.rect.x = round(self._position.x)

        # Colisión Horizontal: Si colisionamos, volvemos atrás
        pushed = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:  # Íbamos a la derecha
                    self.rect.right = wall.left
                elif dx < 0:  # Íbamos a la izquierda
                    self.rect.left = wall.right
                else:
                    continue
                pushed = True
        if pushed:
            self._position.x = self.rect.x

    def _move_vertically(self, dy, walls):
        self._position.y += dy
        self.rect.y = round(self._position.y)

        # Colisión Vertical: Si colisionamos, volvemos atrás
        pushed = False
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:  # Íbamos hacia abajo
                    self.rect.bottom = wall.top
                elif dy < 0:  # Íbamos hacia arriba
                    self.rect.top = wall.bottom
                else:
                    continue
                pushed = True
        if pushed:
            self._position.y = self.rect.y

    def _sync_position(self):
        """Keep the float position aligned with the collision rect."""
        self._position.update(self.rect.topleft)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            # Fallback visual
            pygame.draw.rect(surface, (0, 255, 0), self.rect)

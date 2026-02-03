import pygame
import os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class MapManager:
    def __init__(self):
        # Rutas relativas dinámicas
        self.ruta_base = os.path.dirname(os.path.abspath(__file__))
        self.ruta_assets = os.path.join(self.ruta_base, "assets")
        
        # Cargar imágenes de los tiles
        self.tiles = {
            "W": self.load_tile("wall.png"),
            ".": self.load_tile("floor.png"),
            "T": self.load_tile("terminal.png"),
            "D": self.load_tile("door.png"),
            "DO": self.load_tile("door_open.png"), # Puerta abierta
            "P": self.load_tile("floor.png") # El jugador aparece sobre el suelo
        }
        
        # Mapa 20x12 (1280x768 si TILE_SIZE=64, se recorta un poco abajo o se ajusta)
        # Para 1280x720 exactamente son 20x11.25 tiles, usaremos 20x12 y Pygame SCALED lo ajustará.
        self.map_matrix = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W..................W",
            "W...T..............W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W.........P........W",
            "W..................W",
            "W..................W",
            "W..................W",
            "W..................D",
            "WWWWWWWWWWWWWWWWWWWW"
        ]
        
        self.walls = []
        self.player_spawn = [10 * TILE_SIZE, 6 * TILE_SIZE]
        self.terminal_pos = [4 * TILE_SIZE, 2 * TILE_SIZE]
        self.door_pos = [17 * TILE_SIZE, 10 * TILE_SIZE]
        
        self._build_map()

    def load_tile(self, filename):
        ruta = os.path.join(self.ruta_assets, filename)
        if os.path.exists(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        else:
            print(f"⚠️ Warning: No se encontró el tile: {ruta}")
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((255, 0, 255)) # Color de error
            return surf

    def _build_map(self):
        self.walls = []
        for row_index, row in enumerate(self.map_matrix):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if char == "W":
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == "P":
                    self.player_spawn = [x, y]
                elif char == "T":
                    self.terminal_pos = [x, y]
                elif char == "D":
                    self.door_pos = [x, y]

    def draw(self, screen):
        for row_index, row in enumerate(self.map_matrix):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                # Suelo base
                if char != "W":
                    screen.blit(self.tiles["."], (x, y))
                
                # Tile específico
                if char in self.tiles:
                    # Si es P, ya dibujamos el suelo, no necesitamos dibujar nada más aquí (el jugador se dibuja en engine)
                    if char != "P":
                        screen.blit(self.tiles[char], (x, y))

    def draw_debug(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (255, 0, 0), wall, 2)
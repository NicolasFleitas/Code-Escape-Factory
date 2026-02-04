import pygame
import os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class MapManager:
    def __init__(self):
        # Rutas relativas dinámicas
        self.ruta_base = os.path.dirname(os.path.abspath(__file__))
        self.ruta_assets = os.path.join(self.ruta_base, "assets", "items_mapa")
        
        # Cargar imágenes de los tiles
        self.tiles = {
            "W": self.load_tile("wall.png"),
            ".": self.load_tile("floor.png"),
            "T": self.load_tile("terminal.png"),
            "D": self.load_tile("door.png"),
            "DO": self.load_tile("door_open.png"), # Puerta abierta
            "P": self.load_tile("floor.png"), # El jugador aparece sobre el suelo
            ".": self.load_tile("floor_room1.png"), # Suelo Oficina 1
            ",": self.load_tile("floor_room2.png"), # Suelo Oficina 2
            ":": self.load_tile("floor_room3.png"), # Suelo Oficina 3
            ";": self.load_tile("floor_room4.png"), # Suelo Oficina 4
            "E": self.load_tile("desk.png"), # Escritorio
            "B": self.load_tile("box.png"), # Caja
            "C": self.load_tile("Copy Machine.png"), # Copiadora
            "M": self.load_tile("Mailboxes.png"), # Buzones
            "K": self.load_tile("Water Cooler.png"), # Enfriador de agua
            "Y": self.load_tile("Machinery.png"), # Maquinaria
            "L": self.load_tile("Barrel.png"), # Barril
            "A": self.load_tile("Plant.png"), # Planta
            "S": self.load_tile("Chair.png"), # Silla
            "V": self.load_tile("Vending Machine.png"), # Expendedora
            "X": self.load_tile("Trash Can.png"), # Papelera
            "N": self.load_tile("Industrial Tank.png"), # Tanque
            "H": self.load_tile("Control Panel.png"), # Panel
            "R": self.load_tile("Robot Arm.png"), # Brazo Robot
            "I": self.load_tile("Pipes.png"), # Tuberías
            "-": self.load_tile("floor_pasillo.png") # Suelo pasillo
        }
        
        # Mapa 20x12 (1280x720) - Layout 2x2 Salas
        self.map_matrix = [
            "WWWWWWWWWWWWWWWWWWWW",
            "WAX..C..SWB,,,,,,IIW",
            "W.......TWT,,,,,,,IW",
            "W........WH,,,,,,,,W",
            "W-WWWWWWWWWWWWWWWW-W",
            "W--------P---------D",
            "W--K----------V----W",
            "W-WWWWWWWWWWWWWWWW-W",
            "W::::Y::TWE;R;;;;;;W",
            "W::::::::WE;;;;;;;;W",
            "WA::::::MWT;;;;;;;AW",
            "WWWWWWWWWWWWWWWWWWWW"
        ]



        # Limpieza de espacios para consistencia (usamos '.' para suelo)
        self.map_matrix = [row.replace(" ", ".") for row in self.map_matrix]
        
        self.walls = []
        self.player_spawn = [10 * TILE_SIZE, 6 * TILE_SIZE]
        self.terminals = [] # Lista de posiciones [x, y]
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
        self.terminals = []
        for row_index, row in enumerate(self.map_matrix):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if char in ["W", "E", "B", "C", "M", "K", "Y", "L", "A", "V", "N", "H", "R"]:
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == "P":
                    self.player_spawn = [x, y]
                elif char == "T":
                    self.terminals.append([x, y])
                elif char == "D":
                    self.door_pos = [x, y]

    def _get_floor_type(self, col, row):
        """Determina qué tipo de suelo debe ir en una posición específica."""
        # Si ya es un tipo de suelo en la matriz, lo retornamos
        char = self.map_matrix[row][col]
        if char in [".", ",", ":", ";", "-"]:
            return char

        
        # Lógica de detección por coordenadas para objetos no-suelo
        if row in [4, 5, 6]: return "-" # Pasillo
        if row < 4:
            return "." if col < 9 else "," # Oficina 1 o 2 (el muro está en col 9)
        if row > 6:
            return ":" if col < 9 else ";" # Oficina 3 o 4
        
        return "." # Fallback default

    def draw(self, screen):
        for row_index, row in enumerate(self.map_matrix):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                # 1. Dibujar Suelo Base
                if char != "W":
                    floor_type = self._get_floor_type(col_index, row_index)
                    screen.blit(self.tiles[floor_type], (x, y))
                
                # 2. Dibujar Objeto encima (si no es suelo puro)
                if char in self.tiles and char not in [".", ",", ":", ";", "-", "P"]:
                    screen.blit(self.tiles[char], (x, y))

    def draw_debug(self, screen):

        for wall in self.walls:
            pygame.draw.rect(screen, (255, 0, 0), wall, 2)
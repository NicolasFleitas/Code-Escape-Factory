import pygame
import os

def create_assets():
    pygame.init()
    tile_size = 64
    assets_dir = os.path.join("src", "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # 1. Piso Metálico
    floor = pygame.Surface((tile_size, tile_size))
    floor.fill((100, 100, 105)) # Gris metálico
    # Añadir patrón de rejilla o textura
    for i in range(0, tile_size, 8):
        pygame.draw.line(floor, (80, 80, 85), (i, 0), (i, tile_size))
        pygame.draw.line(floor, (80, 80, 85), (0, i), (tile_size, i))
    pygame.image.save(floor, os.path.join(assets_dir, "floor.png"))

    # 2. Paredes Gris Oscuro
    wall = pygame.Surface((tile_size, tile_size))
    wall.fill((40, 40, 45)) # Gris oscuro
    pygame.draw.rect(wall, (30, 30, 35), (0, 0, tile_size, tile_size), 4) # Borde
    pygame.image.save(wall, os.path.join(assets_dir, "wall.png"))

    # 3. Puerta Roja con Luz Roja (Cerrada)
    door_closed = pygame.Surface((tile_size, tile_size))
    door_closed.fill((150, 30, 30)) # Rojo oscuro
    pygame.draw.rect(door_closed, (100, 20, 20), (5, 5, tile_size-10, tile_size-10), 3)
    # Luz roja
    pygame.draw.circle(door_closed, (255, 0, 0), (tile_size // 2, tile_size // 2), 10)
    pygame.draw.circle(door_closed, (255, 100, 100), (tile_size // 2, tile_size // 2), 5)
    pygame.image.save(door_closed, os.path.join(assets_dir, "door.png"))

    # 4. Puerta con Luz Verde (Abierta)
    door_open = pygame.Surface((tile_size, tile_size))
    door_open.fill((50, 50, 55)) # Fondo oscuro (abierta)
    pygame.draw.rect(door_open, (150, 30, 30), (0, 0, tile_size, tile_size), 4) # Marco rojo
    # Luz verde
    pygame.draw.circle(door_open, (0, 255, 0), (tile_size // 2, tile_size // 2), 10)
    pygame.draw.circle(door_open, (100, 255, 100), (tile_size // 2, tile_size // 2), 5)
    pygame.image.save(door_open, os.path.join(assets_dir, "door_open.png"))

    # 5. Terminal (Extra, para mantenerla funcional)
    terminal = pygame.Surface((tile_size, tile_size))
    terminal.fill((30, 30, 35))
    pygame.draw.rect(terminal, (0, 255, 100), (10, 10, tile_size-20, tile_size-30), 2) # Pantalla
    pygame.draw.rect(terminal, (50, 50, 60), (5, tile_size-15, tile_size-10, 10)) # Teclado
    pygame.image.save(terminal, os.path.join(assets_dir, "terminal.png"))

    print("Assets generados exitosamente en src/assets/")
    pygame.quit()

if __name__ == "__main__":
    create_assets()

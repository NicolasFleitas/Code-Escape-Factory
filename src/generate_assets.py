import pygame
import os

def create_assets():
    pygame.init()
    tile_size = 64
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(ruta_base, "assets", "items_mapa")
    os.makedirs(assets_dir, exist_ok=True)

    def draw_floor(color, shadow_color, filename):
        surf = pygame.Surface((tile_size, tile_size))
        surf.fill(color)
        # Añadir patrón de rejilla o textura
        for i in range(0, tile_size, 16):
            pygame.draw.line(surf, shadow_color, (i, 0), (i, tile_size), 1)
            pygame.draw.line(surf, shadow_color, (0, i), (tile_size, i), 1)
        # Bordes suaves
        pygame.draw.rect(surf, shadow_color, (0, 0, tile_size, tile_size), 1)
        pygame.image.save(surf, os.path.join(assets_dir, filename))

    # 1. Pisos de Oficina (Paleta de Colores)
    # Oficina 1: Azul Industrial
    draw_floor((45, 60, 80), (35, 45, 65), "floor_room1.png")
    # Oficina 2:深板岩 (Pizarra profunda)
    draw_floor((55, 55, 60), (45, 45, 50), "floor_room2.png")
    # Oficina 3: Terracota Mudo
    draw_floor((90, 60, 50), (70, 45, 35), "floor_room3.png")
    # Oficina 4: Verde Musgo/Salvia
    draw_floor((60, 75, 60), (45, 60, 45), "floor_room4.png")
    
    # Suelo General/Default (Gris)
    draw_floor((100, 100, 105), (80, 80, 85), "floor.png")

    # 2. Pasillo (Tecnológico - Más claro y vibrante)
    corridor = pygame.Surface((tile_size, tile_size))
    corridor.fill((60, 80, 100)) # Azul acero claro
    pygame.draw.line(corridor, (0, 200, 255), (0, 0), (tile_size, 0), 2) # Línea de energía cian brillante
    pygame.draw.line(corridor, (0, 200, 255), (0, tile_size-1), (tile_size, tile_size-1), 2)
    # Textura pasillo (rejilla más visible)
    for i in range(0, tile_size, 32):
        pygame.draw.line(corridor, (80, 100, 120), (i, 0), (i, tile_size), 1)
    pygame.image.save(corridor, os.path.join(assets_dir, "floor_pasillo.png"))


    # 3. Paredes Gris Oscuro
    wall = pygame.Surface((tile_size, tile_size))
    wall.fill((40, 40, 45)) 
    pygame.draw.rect(wall, (30, 30, 35), (0, 0, tile_size, tile_size), 4) 
    pygame.image.save(wall, os.path.join(assets_dir, "wall.png"))

    # 4. Puertas y Terminal
    # (Mantenemos la lógica anterior para consistencia)
    door_closed = pygame.Surface((tile_size, tile_size))
    door_closed.fill((150, 30, 30))
    pygame.draw.rect(door_closed, (100, 20, 20), (5, 5, tile_size-10, tile_size-10), 3)
    pygame.draw.circle(door_closed, (255, 0, 0), (tile_size // 2, tile_size // 2), 10)
    pygame.image.save(door_closed, os.path.join(assets_dir, "door.png"))

    door_open = pygame.Surface((tile_size, tile_size))
    door_open.fill((50, 50, 55))
    pygame.draw.rect(door_open, (150, 30, 30), (0, 0, tile_size, tile_size), 4)
    pygame.draw.circle(door_open, (0, 255, 0), (tile_size // 2, tile_size // 2), 10)
    pygame.image.save(door_open, os.path.join(assets_dir, "door_open.png"))

    terminal = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(terminal, (50, 50, 60), (10, 20, 44, 34))
    pygame.draw.rect(terminal, (30, 30, 40), (8, 54, 48, 10))
    pygame.draw.rect(terminal, (0, 40, 0), (14, 24, 36, 26))
    pygame.image.save(terminal, os.path.join(assets_dir, "terminal.png"))

    # 5. Decoraciones
    box = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(box, (139, 69, 19), (8, 8, 48, 48))
    pygame.draw.line(box, (101, 56, 14), (8, 8), (56, 56), 4)
    pygame.draw.line(box, (101, 56, 14), (56, 8), (8, 56), 4)
    pygame.image.save(box, os.path.join(assets_dir, "box.png"))

    desk = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(desk, (70, 70, 80), (4, 15, 56, 40))
    pygame.draw.rect(desk, (50, 50, 60), (4, 15, 56, 40), 2)
    pygame.image.save(desk, os.path.join(assets_dir, "desk.png"))

    # 6. Copiadora (Office)
    copy_m = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(copy_m, (200, 200, 210), (10, 10, 44, 44))
    pygame.draw.rect(copy_m, (150, 150, 160), (10, 25, 44, 5)) # Bandeja
    pygame.draw.rect(copy_m, (50, 50, 60), (15, 12, 10, 5)) # Panel
    pygame.image.save(copy_m, os.path.join(assets_dir, "Copy Machine.png"))

    # 7. Buzones (Office)
    mailb = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(mailb, (120, 120, 130), (5, 5, 54, 54))
    for i in range(10, 50, 12):
        for j in range(10, 50, 12):
            pygame.draw.rect(mailb, (80, 80, 90), (i, j, 8, 8), 1)
            pygame.draw.line(mailb, (180, 180, 190), (i+2, j+4), (i+6, j+4))
    pygame.image.save(mailb, os.path.join(assets_dir, "Mailboxes.png"))

    # 8. Enfriador de Agua (Office)
    cooler = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(cooler, (220, 220, 230), (20, 30, 24, 30)) # Base
    pygame.draw.circle(cooler, (0, 150, 255), (32, 22), 12) # Botella (azul)
    pygame.draw.rect(cooler, (0, 100, 200), (28, 28, 8, 4)) # Cuello
    pygame.image.save(cooler, os.path.join(assets_dir, "Water Cooler.png"))

    # 9. Maquinaria (Factory)
    machinery = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(machinery, (60, 60, 70), (4, 4, 56, 56))
    pygame.draw.circle(machinery, (200, 200, 0), (32, 32), 15, 3) # Engranaje
    pygame.draw.rect(machinery, (255, 50, 50), (10, 10, 6, 6)) # Botón emergencia
    pygame.image.save(machinery, os.path.join(assets_dir, "Machinery.png"))

    # 10. Barril (Factory)
    barrel = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.ellipse(barrel, (180, 120, 50), (12, 4, 40, 56)) # Color óxido/madera
    pygame.draw.ellipse(barrel, (140, 90, 40), (12, 4, 40, 56), 2)
    pygame.draw.line(barrel, (80, 80, 80), (12, 20), (52, 20), 2) # Banda metálica
    pygame.draw.line(barrel, (80, 80, 80), (12, 40), (52, 40), 2)
    pygame.image.save(barrel, os.path.join(assets_dir, "Barrel.png"))

    # 11. Planta de Oficina (Office)
    plant = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(plant, (100, 70, 40), (22, 45, 20, 15)) # Maceta
    pygame.draw.ellipse(plant, (34, 139, 34), (15, 10, 34, 40)) # Hojas verdes
    pygame.draw.ellipse(plant, (0, 100, 0), (20, 5, 24, 35), 2) # Detalle hojas
    pygame.image.save(plant, os.path.join(assets_dir, "Plant.png"))

    # 12. Silla de Oficina (Office)
    chair = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.circle(chair, (40, 40, 45), (32, 32), 18) # Asiento
    pygame.draw.rect(chair, (25, 25, 30), (18, 14, 28, 6)) # Respaldo (top-down view)
    pygame.image.save(chair, os.path.join(assets_dir, "Chair.png"))

    # 13. Máquina Expendedora (Office/Factory)
    vending = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(vending, (50, 50, 60), (10, 5, 44, 54)) # Cuerpo
    pygame.draw.rect(vending, (0, 0, 0), (15, 10, 30, 30)) # Cristal
    pygame.draw.rect(vending, (255, 0, 0), (46, 15, 4, 10)) # Panel lateral
    # Botones/Luces
    pygame.draw.circle(vending, (0, 255, 0), (48, 30), 2)
    pygame.draw.circle(vending, (255, 255, 0), (48, 35), 2)
    pygame.image.save(vending, os.path.join(assets_dir, "Vending Machine.png"))

    # 14. Papelera (Office)
    trash = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.circle(trash, (180, 180, 190), (32, 32), 15) # Cuerpo circular
    pygame.draw.circle(trash, (150, 150, 160), (32, 32), 15, 2) # Borde superior
    pygame.draw.line(trash, (160, 160, 170), (28, 32), (36, 32), 1) # Detalle basura
    pygame.image.save(trash, os.path.join(assets_dir, "Trash Can.png"))

    # 15. Tanque Industrial (Factory - Front View)
    tank = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(tank, (100, 100, 110), (12, 10, 40, 50)) # Cuerpo cilíndrico
    pygame.draw.rect(tank, (150, 150, 160), (12, 10, 40, 10)) # Tapa
    pygame.draw.line(tank, (50, 255, 50), (20, 25), (44, 25), 2) # Nivel de líquido (indicador)
    pygame.image.save(tank, os.path.join(assets_dir, "Industrial Tank.png"))

    # 16. Panel de Control (Factory - Front View)
    panel = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(panel, (50, 50, 55), (8, 15, 48, 45)) # Caja del panel
    pygame.draw.circle(panel, (255, 200, 0), (24, 35), 8) # Indicador analógico
    pygame.draw.line(panel, (0, 0, 0), (24, 35), (28, 30), 2) # Aguja
    pygame.draw.rect(panel, (0, 255, 0), (40, 30, 8, 4)) # Switch 1
    pygame.draw.rect(panel, (255, 0, 0), (40, 40, 8, 4)) # Switch 2
    pygame.image.save(panel, os.path.join(assets_dir, "Control Panel.png"))

    # 17. Brazo Robótico (Factory - Side/Front View)
    robot = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(robot, (200, 200, 0), (20, 50, 24, 10)) # Base
    pygame.draw.line(robot, (150, 150, 0), (32, 50), (32, 25), 4) # Brazo vertical
    pygame.draw.line(robot, (150, 150, 0), (32, 25), (50, 15), 4) # Brazo extendido
    pygame.draw.circle(robot, (50, 50, 60), (50, 15), 6) # Pinza/Herramienta
    pygame.image.save(robot, os.path.join(assets_dir, "Robot Arm.png"))

    # 18. Tuberías (Factory)
    pipes = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    pygame.draw.rect(pipes, (80, 85, 90), (0, 20, 64, 12)) # Tubería horizontal
    pygame.draw.rect(pipes, (100, 105, 110), (20, 20, 8, 12), 1) # Uniones
    pygame.draw.rect(pipes, (100, 105, 110), (40, 20, 8, 12), 1)
    pygame.image.save(pipes, os.path.join(assets_dir, "Pipes.png"))

    print(f"Assets generados exitosamente en {assets_dir}")


    pygame.quit()

if __name__ == "__main__":
    create_assets()

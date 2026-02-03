import pygame
import sys
import os
import math
import random

from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_FONDO,
    COLOR_DOOR, COLOR_DOOR_OPEN, COLOR_SUCCESS, COLOR_ERROR,
    COLOR_TIEMPO, TIEMPO_LIMITE
)

from src.player import Player
from src.terminal import Terminal
from src.puzzle_manager import PuzzleManager
from src.map_manager import MapManager

# --- PALETA INDUSTRIAL ---
MARRON_FABRICA = (110, 70, 45) 
AZUL_ELECTRICO = (0, 150, 255)
BLANCO_BOTON = (255, 255, 255)
NEGRO_TEXTO = (10, 20, 40)

class Game:
    def __init__(self):
        pygame.init()
        # Usamos FULLSCREEN y SCALED para que ocupe toda la pantalla manteniendo la relación de aspecto
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("Code Escape: Factory Reset")
        self.clock = pygame.time.Clock()

        # --- INICIALIZAR GESTOR DE MAPAS ---
        self.map_manager = MapManager()

        # --- INICIALIZAR JUGADOR ---
        self.player = Player(x=self.map_manager.player_spawn[0], y=self.map_manager.player_spawn[1])

        # Fuentes
        self.font_ui = pygame.font.SysFont("monospace", 20)
        self.font_final = pygame.font.SysFont("monospace", 40, bold=True)
        self.font_pixel = pygame.font.SysFont("monospace", 50, bold=True)
        self.font_botones = pygame.font.SysFont("verdana", 18, bold=True)

        # Carga de Fondo
        try:
            ruta_fondo = os.path.join("src", "assets", "menu.png")
            self.fondo_menu = pygame.image.load(ruta_fondo).convert()
            self.fondo_menu = pygame.transform.scale(self.fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.fondo_menu = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.fondo_menu.fill((30, 30, 35))

        self.opciones = ["START GAME", "EXIT"]
        self.botones_rects = []
        self.setup_botones()
        
        # Instancias
        self.pc_terminal = Terminal(self.map_manager.terminal_pos[0], self.map_manager.terminal_pos[1], task_id=1)
        self.puzzle = PuzzleManager()

        # Propiedades de la Puerta
        from src.settings import TILE_SIZE
        self.door_rect = pygame.Rect(self.map_manager.door_pos[0], self.map_manager.door_pos[1], TILE_SIZE, TILE_SIZE)
        self.puerta_abierta = False

        # Lógica de Tiempo
        self.inicio_ticks = pygame.time.get_ticks()

        # Estados: "MENU, "EXPLORANDO", "PROGRAMANDO", "PERDIDO", "GANASTE"
        self.game_state = "MENU"
        self.tiempo_restante = TIEMPO_LIMITE
    
    def setup_botones(self):
        """ Configuración de botones """
        ancho_b, alto_b = 250, 45 
        x = SCREEN_WIDTH // 2 - ancho_b // 2
        y_inicial = 480  
        for i in range(len(self.opciones)):
            rect = pygame.Rect(x, y_inicial + (i * 70), ancho_b, alto_b)
            self.botones_rects.append(rect)
    
    def draw_curved_text(self, text, center_x, center_y, radius):
        """Dibuja el título curvado en la parte superior (cielo)."""
        arc_angle = 80
        start_angle = -90 - (arc_angle / 2)
        for i, char in enumerate(text):
            angle = start_angle + (i * (arc_angle / (len(text) - 1)))
            rad = math.radians(angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            char_surf = self.font_pixel.render(char, False, MARRON_FABRICA)
            char_surf = pygame.transform.rotate(char_surf, -angle - 90)
            self.screen.blit(char_surf, char_surf.get_rect(center=(x, y)))
    
    def dibujar_entorno_obrero(self, x, y, frame_up):
        """Obreros martillando yunque con chispas."""
        pygame.draw.rect(self.screen, (80, 85, 90), (x + 35, y + 15, 55, 15)) # Yunque
        pygame.draw.rect(self.screen, (40, 70, 140), (x, y, 24, 34))         # Cuerpo
        pygame.draw.rect(self.screen, (255, 205, 160), (x + 2, y - 18, 20, 18)) # Cara
        pygame.draw.rect(self.screen, (255, 160, 0), (x - 2, y - 22, 28, 10))   # Casco
        
        angle = -40 if frame_up else 15
        pygame.draw.rect(self.screen, (255, 205, 160), (x + 18, y + 5 + angle, 15, 8)) # Brazo
        pygame.draw.rect(self.screen, (150, 150, 160), (x + 28, y - 12 + angle, 18, 12)) # Martillo
        
        if not frame_up: # Efecto de chispas al golpear
            for _ in range(3):
                pygame.draw.rect(self.screen, (255, 200, 0), (x+50+random.randint(0,20), y+15+random.randint(-5,5), 3, 3))

    def draw_welcome_screen(self):
        self.screen.blit(self.fondo_menu, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        ticks = pygame.time.get_ticks()
        frame_up = (ticks // 300) % 2 == 0

        # Título arriba en el cielo
        self.draw_curved_text("CODE FACTORY", SCREEN_WIDTH // 2, 400, 360)

        # Obreros martillando (reposicionados para 720p)
        self.dibujar_entorno_obrero(SCREEN_WIDTH // 5, 530, frame_up)
        self.dibujar_entorno_obrero(4 * SCREEN_WIDTH // 5, 530, not frame_up)

        # Botones con letras en movimiento
        for i, rect in enumerate(self.botones_rects):
            hover = rect.collidepoint(mouse_pos)
            color = (230, 245, 255) if hover else BLANCO_BOTON
            pygame.draw.rect(self.screen, AZUL_ELECTRICO, rect.inflate(4, 4))
            pygame.draw.rect(self.screen, color, rect)
            
            label = self.font_botones.render(self.opciones[i], True, NEGRO_TEXTO)
            self.screen.blit(label, (rect.centerx - label.get_width() // 2, 
                                     rect.centery - label.get_height() // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.game_state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.botones_rects):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        if i == 0: self.game_state = "EXPLORANDO"
                        else: pygame.quit(); sys.exit()

            if self.game_state == "EXPLORANDO":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    # CARGAMOS EL PUZZLE SEGÚN EL ID DE LA TERMINAL
                    self.puzzle.set_puzzle(self.pc_terminal.task_id)
                    self.game_state = "PROGRAMANDO"

            elif self.game_state == "PROGRAMANDO":
                result = self.puzzle.handle_event(event)
                if result == "SOLVED":
                    self.puerta_abierta = True
                    # No regresamos inmediatamente para que el usuario vea el éxito

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state = "EXPLORANDO"

    def update(self):
        # --- Gestión de Tiempo ---
        if self.game_state not in ["PERDIDO", "GANASTE"]:
            segundos_transcurridos = (
                pygame.time.get_ticks() - self.inicio_ticks
            ) // 1000
            self.tiempo_restante = max(0, TIEMPO_LIMITE - segundos_transcurridos)

            if self.tiempo_restante <= 0:
                self.game_state = "PERDIDO"

        # --- Lógica de Movimiento y Victoria ---
        if self.game_state == "EXPLORANDO":
            self.player.update(self.map_manager.walls)

            # Si la puerta está cerrada, bloquea el paso
            if not self.puerta_abierta:
                if self.player.rect.colliderect(self.door_rect):
                    self.player.rect.right = self.door_rect.left
            else:
                # Si la puerta está ABIERTA y el jugador la toca -> ¡GANA!
                if self.player.rect.colliderect(self.door_rect):
                    self.game_state = "GANASTE"

    def draw(self):
        # self.screen.fill(COLOR_FONDO) # El mapa ya llena la pantalla
        self.map_manager.draw(self.screen)

        if self.game_state != "PERDIDO" and self.game_state != "GANASTE":
            # 1. Dibujar Puerta (Cambia de tile según el estado)
            if self.puerta_abierta:
                self.screen.blit(self.map_manager.tiles["DO"], self.door_rect)
            else:
                self.screen.blit(self.map_manager.tiles["D"], self.door_rect)

            # 2. Dibujar Elementos
            self.pc_terminal.draw(self.screen, self.player.rect)
            self.player.draw(self.screen)

            # 3. Dibujar UI de Energía
            timer_text = self.font_ui.render(
                f"ENERGIA LINTERNA: {self.tiempo_restante}s", True, COLOR_TIEMPO
            )
            self.screen.blit(timer_text, (20, 20))

            # 4. Overlay de Terminal
            if self.game_state == "PROGRAMANDO":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(230)
                overlay.fill((5, 10, 5))
                self.screen.blit(overlay, (0, 0))
                self.puzzle.draw(self.screen)

        elif self.game_state == "PERDIDO":
            self.screen.fill((0, 0, 0))
            msg = self.font_final.render("LINTERNA APAGADA", True, COLOR_ERROR)
            msg_sub = self.font_ui.render(
                "Te has quedado atrapado en la oscuridad.", True, (100, 100, 100)
            )
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(
                msg_sub, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 30)
            )

        elif self.game_state == "GANASTE":
            self.screen.fill((20, 50, 20))  # Fondo verde oscuro
            msg = self.font_final.render("¡GANASTE!", True, COLOR_SUCCESS)
            msg_sub = self.font_ui.render(
                "Has escapado de la fabrica a tiempo.", True, (255, 255, 255)
            )
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(
                msg_sub, (SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 30)
            )

        pygame.display.flip()

    def run(self):
        """ Bucle principal del juego """
        while True:
            self.handle_events() # Crucial para que la ventana no se cuelgue
            
            if self.game_state == "MENU":
                self.draw_welcome_screen()
                pygame.display.flip() # Necesitas actualizar la pantalla aquí también
            else:
                self.update()
                self.draw()
                
            self.clock.tick(FPS)

import pygame
import math
import random
import os
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MARRON_FABRICA, AZUL_ELECTRICO, 
    BLANCO_BOTON, NEGRO_TEXTO, COLOR_TIEMPO, COLOR_SUCCESS, COLOR_ERROR
)

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self._setup_fonts()
        self._setup_assets()

    def _setup_fonts(self):
        self.font_ui = pygame.font.SysFont("monospace", 20)
        self.font_final = pygame.font.SysFont("monospace", 40, bold=True)
        self.font_pixel = pygame.font.SysFont("monospace", 50, bold=True)
        self.font_botones = pygame.font.SysFont("verdana", 18, bold=True)

    def _setup_assets(self):
        try:
            ruta_fondo = os.path.join("src", "assets", "menu.png")
            self.fondo_menu = pygame.image.load(ruta_fondo).convert()
            self.fondo_menu = pygame.transform.scale(self.fondo_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.fondo_menu = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.fondo_menu.fill((30, 30, 35))

    def draw_curved_text(self, text, center_x, center_y, radius):
        """Dibuja el título curvado en la parte superior."""
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
        
        if not frame_up:
            self._draw_sparks(x + 50, y + 15)

    def _draw_sparks(self, x, y):
        for _ in range(3):
            pygame.draw.rect(self.screen, (255, 200, 0), (x + random.randint(0, 20), y + random.randint(-5, 5), 3, 3))

    def draw_menu_buttons(self, opciones, botones_rects, selected_option):
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(botones_rects):
            hover = rect.collidepoint(mouse_pos)
            selected = (i == selected_option)
            
            color = (230, 245, 255) if (hover or selected) else BLANCO_BOTON
            border_color = (255, 200, 0) if selected else AZUL_ELECTRICO
            border_width = 6 if selected else 4
            
            pygame.draw.rect(self.screen, border_color, rect.inflate(border_width, border_width))
            pygame.draw.rect(self.screen, color, rect)
            
            label = self.font_botones.render(opciones[i], True, NEGRO_TEXTO)
            self.screen.blit(label, (rect.centerx - label.get_width() // 2, 
                                     rect.centery - label.get_height() // 2))

    def draw_welcome_screen(self, opciones, botones_rects, selected_option):
        self.screen.blit(self.fondo_menu, (0, 0))
        ticks = pygame.time.get_ticks()
        frame_up = (ticks // 300) % 2 == 0

        self.draw_curved_text("CODE FACTORY", SCREEN_WIDTH // 2, 400, 360)
        self.dibujar_entorno_obrero(SCREEN_WIDTH // 5, 530, frame_up)
        self.dibujar_entorno_obrero(4 * SCREEN_WIDTH // 5, 530, not frame_up)
        self.draw_menu_buttons(opciones, botones_rects, selected_option)

    def draw_gameplay_ui(self, tiempo_restante, terminals):
        # Energía
        timer_text = self.font_ui.render(f"Tiempo restante: {tiempo_restante}s", True, COLOR_TIEMPO)
        self.screen.blit(timer_text, (20, 20))
        
        # Terminales resueltas
        solved_count = sum(1 for t in terminals if t.solved)
        progress_text = self.font_ui.render(f"Misiones: {solved_count}/{len(terminals)}", True, (0, 255, 255))
        self.screen.blit(progress_text, (20, 50))

    def draw_programming_overlay(self, puzzle_manager):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((5, 10, 5))
        self.screen.blit(overlay, (0, 0))
        puzzle_manager.draw(self.screen)

    def draw_pause_screen(self, opciones, botones_rects, selected_option):
        # Fondo semitransparente oscuro
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Título
        titulo = self.font_pixel.render("PAUSA", True, BLANCO_BOTON)
        self.screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 150))
        
        # Botones
        self.draw_menu_buttons(opciones, botones_rects, selected_option)

    def draw_end_screen(self, game_state, opciones=None, botones_rects=None, selected_option=0):
        if game_state == "PERDIDO":
            self._render_end_msg("PERDISTE", "Te has quedado encerrado en la fabrica.", COLOR_ERROR, (0, 0, 0))
        elif game_state == "GANASTE":
            self._render_end_msg("¡GANASTE!", "Has escapado de la fabrica a tiempo.", COLOR_SUCCESS, (20, 50, 20))
        
        if opciones and botones_rects:
            self.draw_menu_buttons(opciones, botones_rects, selected_option)

    def _render_end_msg(self, title, subtitle, title_color, bg_color):
        self.screen.fill(bg_color)
        msg = self.font_final.render(title, True, title_color)
        msg_sub = self.font_ui.render(subtitle, True, (255, 255, 255) if title_color != COLOR_ERROR else (100, 100, 100))
        self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(msg_sub, (SCREEN_WIDTH // 2 - msg_sub.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

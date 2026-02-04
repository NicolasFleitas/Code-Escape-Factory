import pygame
import sys
import os
import math
import random

from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_FONDO,
    COLOR_DOOR, COLOR_DOOR_OPEN, COLOR_SUCCESS, COLOR_ERROR,
    COLOR_TIEMPO, TIEMPO_LIMITE, TILE_SIZE,
    MARRON_FABRICA, AZUL_ELECTRICO, BLANCO_BOTON, NEGRO_TEXTO
)

from src.player import Player
from src.terminal import Terminal
from src.puzzle_manager import PuzzleManager
from src.map_manager import MapManager
from src.audio_manager import AudioManager
from src.ui_manager import UIManager
from src.character_selector import CharacterSelector

class Game:
    def __init__(self):
        self._init_pygame()
        
        # Managers
        self.audio_manager = AudioManager()
        self.audio_manager.setup()
        
        self.ui_manager = UIManager(self.screen)
        self.map_manager = MapManager()
        self.puzzle = PuzzleManager()
        self.character_selector = CharacterSelector(self.screen)

        # Legacy attributes (preserving identifiers)
        self.victoria_sound = self.audio_manager.victoria_sound
        self.derrota_sound = self.audio_manager.derrota_sound
        self.alarma_sound = self.audio_manager.alarma_sound
        
        self.font_ui = self.ui_manager.font_ui
        self.font_final = self.ui_manager.font_final
        self.font_pixel = self.ui_manager.font_pixel
        self.font_botones = self.ui_manager.font_botones
        self.fondo_menu = self.ui_manager.fondo_menu

        self._setup_entities()
        self._setup_state()


    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("Code Escape: Factory Reset")
        self.clock = pygame.time.Clock()

    def _setup_entities(self):
        self.player = Player(x=self.map_manager.player_spawn[0], y=self.map_manager.player_spawn[1])
        self.terminals = [Terminal(pos[0], pos[1], task_id=i+1) for i, pos in enumerate(self.map_manager.terminals)]
        self.active_terminal = None
        self.door_rect = pygame.Rect(self.map_manager.door_pos[0], self.map_manager.door_pos[1], TILE_SIZE, TILE_SIZE)
        self.puerta_abierta = False

    def _setup_state(self):
        self.game_state = "MENU"  # Comienza en el Menú Principal
        self.opciones = ["START GAME", "EXIT"]
        self.botones_rects = []
        self.selected_option = 0
        self.tiempo_restante = TIEMPO_LIMITE
        self.inicio_ticks = None
        
        # Banderas de control (mapeadas al audio_manager para consistencia si se desea, 
        # pero mantenidas aquí para "preserve_variable_names")
        self.victoria_sound_played = False
        self.victoria_sound_start_time = None
        self.derrota_sound_played = False
        self.derrota_sound_start_time = None
        self.alarma_10s_played = False
        self.alarma_5s_played = False

        self.opciones_final = ["RESTART", "MENU"]
        self.botones_final_rects = []
        self.selected_final_option = 0
        
        self.setup_botones()
        self.setup_botones_final()


    # --- Legacy Methods (Proxies to Managers) ---

    def setup_botones(self):
        """ Configuración de botones """
        ancho_b, alto_b = 250, 45 
        x = SCREEN_WIDTH // 2 - ancho_b // 2
        y_inicial = 480  
        self.botones_rects = []
        for i in range(len(self.opciones)):
            rect = pygame.Rect(x, y_inicial + (i * 70), ancho_b, alto_b)
            self.botones_rects.append(rect)

    def setup_botones_final(self):
        """ Configuración de botones para la pantalla de victoria/derrota """
        ancho_b, alto_b = 200, 45
        espaciado = 250
        ancho_total = (len(self.opciones_final) - 1) * espaciado
        x_inicio = (SCREEN_WIDTH - ancho_total) // 2 - (ancho_b // 2)
        y = SCREEN_HEIGHT // 2 + 100
        
        self.botones_final_rects = []
        for i in range(len(self.opciones_final)):
            rect = pygame.Rect(x_inicio + (i * espaciado), y, ancho_b, alto_b)
            self.botones_final_rects.append(rect)

    def draw_curved_text(self, text, center_x, center_y, radius):
        self.ui_manager.draw_curved_text(text, center_x, center_y, radius)

    def dibujar_entorno_obrero(self, x, y, frame_up):
        self.ui_manager.dibujar_entorno_obrero(x, y, frame_up)

    def draw_welcome_screen(self):
        self.ui_manager.draw_welcome_screen(self.opciones, self.botones_rects, self.selected_option)

    # --- Event Handling ---

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            
            if self.game_state == "CHARACTER_SELECT":
                # Manejar selección de personajes
                if self.character_selector.handle_event(event):
                    # Configurar sprites del jugador según la selección
                    # Indice 0 -> Obrero 1, Indice 1 -> Obrero 2, etc.
                    self.player.load_sprites(character_id=self.character_selector.indice_seleccionado + 1)
                    
                    # Selección completada, iniciar juego
                    self.game_state = "EXPLORANDO"
                    self.inicio_ticks = pygame.time.get_ticks()  # Iniciar tiempo aquí
            elif self.game_state == "MENU":
                self._handle_menu_events(event)
            elif self.game_state == "EXPLORANDO":
                self._handle_exploration_events(event)
            elif self.game_state == "PROGRAMANDO":
                self._handle_programming_events(event)
            elif self.game_state in ["GANASTE", "PERDIDO"]:
                self._handle_final_events(event)

    def _handle_final_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_final_option = (self.selected_final_option - 1) % len(self.opciones_final)
            elif event.key == pygame.K_RIGHT:
                self.selected_final_option = (self.selected_final_option + 1) % len(self.opciones_final)
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                self._select_final_option()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.botones_final_rects):
                if rect.collidepoint(event.pos):
                    self.selected_final_option = i
                    self._select_final_option()
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.botones_final_rects):
                if rect.collidepoint(event.pos):
                    self.selected_final_option = i

    def _select_final_option(self):
        if self.selected_final_option == 0:  # RESTART
            self.reset_game()
            self.game_state = "CHARACTER_SELECT"
        else:  # MENU
            self.reset_game()
            self.game_state = "MENU"

    def reset_game(self):
        """ Reinicia el estado del juego para una nueva partida """
        self._setup_entities()
        self._setup_state()
        self.active_terminal = None
        self.puerta_abierta = False
        pygame.mixer.music.unpause()
        
        # Reset flags de sonido específicamente
        self.victoria_sound_played = False
        self.derrota_sound_played = False
        self.alarma_10s_played = False
        self.alarma_5s_played = False
        
        # Asegurarse de que el selector de personajes también se reinicie
        self.character_selector.en_menu = True
        self.character_selector.indice_seleccionado = 0
        self.character_selector.personaje_elegido = None
        self.character_selector.imagen_elegida = None

    def _handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.opciones)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.opciones)
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                self._select_menu_option()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.botones_rects):
                if rect.collidepoint(event.pos):
                    self.selected_option = i
                    self._select_menu_option()
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.botones_rects):
                if rect.collidepoint(event.pos):
                    self.selected_option = i

    def _select_menu_option(self):
        if self.selected_option == 0:
            # Ir a selección de personaje en lugar de directo al juego
            self.game_state = "CHARACTER_SELECT"
            # Nota: El tiempo no inicia aquí, sino después de seleccionar personaje
        else:
            self._quit()

    def _handle_exploration_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            for t in self.terminals:
                if t.is_player_near(self.player.rect):
                    self.active_terminal = t
                    self.puzzle.set_puzzle(t.task_id)
                    self.game_state = "PROGRAMANDO"
                    break

    def _handle_programming_events(self, event):
        result = self.puzzle.handle_event(event)
        if result == "SOLVED":
            if self.active_terminal:
                self.active_terminal.solved = True
            if all(t.solved for t in self.terminals):
                self.puerta_abierta = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_state = "EXPLORANDO"

    def _quit(self):
        pygame.quit()
        sys.exit()

    # --- Logic ---

    def update(self):
        self._update_timer()
        self._update_audio_sync()
        self._update_movement()

    def _update_timer(self):
        if self.game_state not in ["PERDIDO", "GANASTE"] and self.inicio_ticks is not None:
            segundos_transcurridos = (pygame.time.get_ticks() - self.inicio_ticks) // 1000
            self.tiempo_restante = max(0, TIEMPO_LIMITE - segundos_transcurridos)
            
            # Alarmas (usando manager pero manteniendo estados locales para persistencia)
            if self.alarma_sound:
                if 5 < self.tiempo_restante <= 10 and not self.alarma_10s_played:
                    self.alarma_sound.play()
                    self.alarma_10s_played = True
                if 0 < self.tiempo_restante <= 5 and not self.alarma_5s_played:
                    self.alarma_sound.play()
                    self.alarma_5s_played = True

            if self.tiempo_restante <= 0:
                self.game_state = "PERDIDO"
                if self.derrota_sound and not self.derrota_sound_played:
                    pygame.mixer.music.pause()
                    self.derrota_sound.play()
                    self.derrota_sound_played = True
                    self.derrota_sound_start_time = pygame.time.get_ticks()

    def _update_audio_sync(self):
        # Sincronización de victoria
        if self.victoria_sound_start_time is not None:
            if self.audio_manager.check_sound_completion(self.victoria_sound_start_time, self.victoria_sound):
                self.victoria_sound_start_time = None
        
        # Sincronización de derrota
        if self.derrota_sound_start_time is not None:
            if self.audio_manager.check_sound_completion(self.derrota_sound_start_time, self.derrota_sound):
                self.derrota_sound_start_time = None

    def _update_movement(self):
        if self.game_state == "EXPLORANDO":
            self.player.update(self.map_manager.walls)
            if not self.puerta_abierta:
                if self.player.rect.colliderect(self.door_rect):
                    self.player.rect.right = self.door_rect.left
            else:
                if self.player.rect.colliderect(self.door_rect):
                    self.game_state = "GANASTE"
                    if self.victoria_sound and not self.victoria_sound_played:
                        pygame.mixer.music.pause()
                        self.victoria_sound.play()
                        self.victoria_sound_played = True
                        self.victoria_sound_start_time = pygame.time.get_ticks()

    # --- Drawing ---

    def draw(self):
        self.map_manager.draw(self.screen)

        if self.game_state not in ["PERDIDO", "GANASTE"]:
            self._draw_gameplay()
        else:
            self.ui_manager.draw_end_screen(
                self.game_state, 
                opciones=self.opciones_final, 
                botones_rects=self.botones_final_rects, 
                selected_option=self.selected_final_option
            )

        pygame.display.flip()

    def _draw_gameplay(self):
        # Puerta
        door_tile = self.map_manager.tiles["DO"] if self.puerta_abierta else self.map_manager.tiles["D"]
        self.screen.blit(door_tile, self.door_rect)

        # Elementos
        for t in self.terminals:
            t.draw(self.screen, self.player.rect)
        self.player.draw(self.screen)

        # UI
        self.ui_manager.draw_gameplay_ui(self.tiempo_restante, self.terminals)

        # Overlay Terminal
        if self.game_state == "PROGRAMANDO":
            self.ui_manager.draw_programming_overlay(self.puzzle)

    def run(self):
        """ Bucle principal del juego """
        while True:
            self.handle_events()
            if self.game_state == "CHARACTER_SELECT":
                self.character_selector.dibujar_menu()
                pygame.display.flip()
            elif self.game_state == "MENU":
                self.draw_welcome_screen()
                pygame.display.flip()
            else:
                self.update()
                self.draw()
            self.clock.tick(FPS)

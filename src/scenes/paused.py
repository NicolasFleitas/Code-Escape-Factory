"""Pause overlay scene."""

import pygame

from src.game_state import GameState
from src.scenes.base import BaseScene
from src.settings import SCREEN_WIDTH


class PausedScene(BaseScene):
    """Frozen gameplay with the CONTINUAR / SALIR menu."""

    OPTIONS = ["CONTINUAR", "SALIR"]

    def __init__(self, game):
        super().__init__(game)
        self.opciones_pausa = list(self.OPTIONS)
        self.selected_pausa_option = 0
        self.botones_pausa_rects = self._build_buttons()

    def _build_buttons(self):
        width, height = 200, 45
        y_initial = 250
        x = SCREEN_WIDTH // 2 - width // 2
        return [
            pygame.Rect(x, y_initial + (i * 80), width, height)
            for i in range(len(self.opciones_pausa))
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_pausa_option = (self.selected_pausa_option - 1) % len(
                    self.opciones_pausa
                )
            elif event.key == pygame.K_DOWN:
                self.selected_pausa_option = (self.selected_pausa_option + 1) % len(
                    self.opciones_pausa
                )
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._select_option()
            elif event.key == pygame.K_ESCAPE:
                # Pressing ESC again resumes the game.
                self.selected_pausa_option = 0
                self._resume()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.botones_pausa_rects):
                if rect.collidepoint(event.pos):
                    self.selected_pausa_option = i
                    self._select_option()
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.botones_pausa_rects):
                if rect.collidepoint(event.pos):
                    self.selected_pausa_option = i

    def _select_option(self):
        if self.selected_pausa_option == 0:  # CONTINUAR
            self._resume()
        else:  # SALIR
            self.game.reset_game()
            self.game.change_state(GameState.MENU)

    def _resume(self):
        """Resume the run, shifting the timer by the time spent paused."""
        game = self.game
        paused_for = pygame.time.get_ticks() - game.pausa_start_time
        game.inicio_ticks += paused_for
        game.change_state(GameState.PLAYING)
        pygame.mixer.music.unpause()

    def update(self, dt):
        # Only the music-sync bookkeeping runs while paused.
        self._update_audio_sync()

    def draw(self):
        self._draw_world()
        self._draw_gameplay()
        self.game.ui_manager.draw_pause_screen(
            self.opciones_pausa,
            self.botones_pausa_rects,
            self.selected_pausa_option,
        )

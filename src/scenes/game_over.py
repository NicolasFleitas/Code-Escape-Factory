"""Victory / defeat end scene."""

import pygame

from src.game_state import GameState
from src.scenes.base import BaseScene
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH


class GameOverScene(BaseScene):
    """End screen shown for WON and LOST, with RESTART / MENU options."""

    OPTIONS = ["RESTART", "MENU"]

    def __init__(self, game, outcome):
        super().__init__(game)
        if outcome not in (GameState.WON, GameState.LOST):
            raise ValueError(f"invalid end outcome: {outcome!r}")
        self.outcome = outcome
        self.opciones_final = list(self.OPTIONS)
        self.selected_final_option = 0
        self.botones_final_rects = self._build_buttons()

    def _build_buttons(self):
        width, height = 200, 45
        spacing = 250
        total_width = (len(self.OPTIONS) - 1) * spacing
        x_start = (SCREEN_WIDTH - total_width) // 2 - (width // 2)
        y = SCREEN_HEIGHT // 2 + 100
        return [
            pygame.Rect(x_start + (i * spacing), y, width, height)
            for i in range(len(self.OPTIONS))
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_final_option = (self.selected_final_option - 1) % len(
                    self.opciones_final
                )
            elif event.key == pygame.K_RIGHT:
                self.selected_final_option = (self.selected_final_option + 1) % len(
                    self.opciones_final
                )
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._select_option()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.botones_final_rects):
                if rect.collidepoint(event.pos):
                    self.selected_final_option = i
                    self._select_option()
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.botones_final_rects):
                if rect.collidepoint(event.pos):
                    self.selected_final_option = i

    def _select_option(self):
        self.game.reset_game()
        if self.selected_final_option == 0:  # RESTART
            self.game.change_state(GameState.CHARACTER_SELECT)
        else:  # MENU
            self.game.change_state(GameState.MENU)

    def update(self, dt):
        # Only the music-sync bookkeeping runs on the end screen.
        self._update_audio_sync()

    def draw(self):
        self._draw_world()
        self.game.ui_manager.draw_end_screen(
            self.outcome,
            opciones=self.opciones_final,
            botones_rects=self.botones_final_rects,
            selected_option=self.selected_final_option,
        )

"""Main menu scene."""

import pygame

from src.game_state import GameState
from src.scenes.base import BaseScene
from src.settings import SCREEN_WIDTH


class MenuScene(BaseScene):
    """Title screen with the START GAME / EXIT options."""

    OPTIONS = ["START GAME", "EXIT"]

    def __init__(self, game):
        super().__init__(game)
        self.opciones = list(self.OPTIONS)
        self.selected_option = 0
        self.botones_rects = self._build_buttons()

    def _build_buttons(self):
        width, height = 250, 45
        x = SCREEN_WIDTH // 2 - width // 2
        y_initial = 480
        return [
            pygame.Rect(x, y_initial + (i * 70), width, height)
            for i in range(len(self.opciones))
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.opciones)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.opciones)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._select_option()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.botones_rects):
                if rect.collidepoint(event.pos):
                    self.selected_option = i
                    self._select_option()
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.botones_rects):
                if rect.collidepoint(event.pos):
                    self.selected_option = i

    def _select_option(self):
        if self.selected_option == 0:
            # The run timer does not start here; it starts after the
            # character selection completes.
            self.game.change_state(GameState.CHARACTER_SELECT)
        else:
            self.game.quit()

    def update(self, dt):
        pass

    def draw(self):
        self.game.ui_manager.draw_welcome_screen(
            self.opciones, self.botones_rects, self.selected_option
        )

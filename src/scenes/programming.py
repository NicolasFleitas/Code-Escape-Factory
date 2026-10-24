"""Terminal programming (puzzle) scene."""

import pygame

from src.game_state import GameState
from src.scenes.base import BaseScene


class ProgrammingScene(BaseScene):
    """The player types the puzzle solution into the active terminal."""

    def handle_event(self, event):
        result = self.game.puzzle.handle_event(event)
        if result == "SOLVED":
            if self.game.active_terminal:
                self.game.active_terminal.solved = True
            if all(t.solved for t in self.game.terminals):
                self.game.puerta_abierta = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state(GameState.PLAYING)

    def update(self, dt):
        # The countdown keeps running while programming; movement does not.
        self._update_timer()
        self._update_audio_sync()

    def draw(self):
        self._draw_world()
        self._draw_gameplay()
        self.game.ui_manager.draw_programming_overlay(self.game.puzzle)

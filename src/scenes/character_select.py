"""Character selection scene."""

import pygame

from src.game_state import GameState
from src.scenes.base import BaseScene


class CharacterSelectScene(BaseScene):
    """Lets the player pick a worker before the run starts."""

    def handle_event(self, event):
        selector = self.game.character_selector
        if selector.handle_event(event):
            # Character ids are 1-based: selection 0 -> worker 1.
            self.game.player.load_sprites(
                character_id=selector.indice_seleccionado + 1
            )
            self.game.change_state(GameState.PLAYING)
            # The run timer starts here, not in the menu.
            self.game.inicio_ticks = pygame.time.get_ticks()

    def update(self, dt):
        pass

    def draw(self):
        self.game.character_selector.dibujar_menu()

"""Shared behavior for all game scenes."""

import pygame

from src.game_state import GameState
from src.settings import COLOR_FONDO, TIEMPO_LIMITE


class BaseScene:
    """Base class for every game state scene.

    Each scene owns the event handling, update, and drawing of one
    GameState. Shared per-run state (timer, entities, sound flags) lives
    on Game and is reached through ``self.game``.
    """

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        """Handle a single pygame event. Override in subclasses."""

    def update(self, dt):
        """Advance the scene by dt seconds. Override in subclasses."""

    def draw(self):
        """Render the scene. Override in subclasses."""

    # --- Shared helpers ---

    def _update_timer(self):
        """Count down the run timer; trigger LOST when it reaches zero."""
        game = self.game
        if game.inicio_ticks is None:
            return

        elapsed_seconds = (pygame.time.get_ticks() - game.inicio_ticks) // 1000
        game.tiempo_restante = max(0, TIEMPO_LIMITE - elapsed_seconds)

        audio = game.audio_manager
        if audio.alarma_sound:
            if 5 < game.tiempo_restante <= 10 and not game.alarma_10s_played:
                audio.alarma_sound.play()
                game.alarma_10s_played = True
            if 0 < game.tiempo_restante <= 5 and not game.alarma_5s_played:
                audio.alarma_sound.play()
                game.alarma_5s_played = True

        if game.tiempo_restante <= 0:
            game.change_state(GameState.LOST)
            if audio.derrota_sound and not game.derrota_sound_played:
                pygame.mixer.music.pause()
                audio.derrota_sound.play()
                game.derrota_sound_played = True
                game.derrota_sound_start_time = pygame.time.get_ticks()

    def _update_audio_sync(self):
        """Resume the background music once the victory/defeat sound ended."""
        game = self.game
        audio = game.audio_manager

        if game.victoria_sound_start_time is not None:
            if audio.check_sound_completion(
                game.victoria_sound_start_time, audio.victoria_sound
            ):
                game.victoria_sound_start_time = None

        if game.derrota_sound_start_time is not None:
            if audio.check_sound_completion(
                game.derrota_sound_start_time, audio.derrota_sound
            ):
                game.derrota_sound_start_time = None

    def _draw_world(self):
        """Draw the background color and the map."""
        game = self.game
        game.screen.fill(COLOR_FONDO)
        game.map_renderer.draw(game.screen)

    def _draw_gameplay(self):
        """Draw the door, terminals, player, and the gameplay UI."""
        game = self.game
        door_tile = game.map_renderer.door_tile(game.puerta_abierta)
        game.screen.blit(door_tile, game.door_rect)

        for terminal in game.terminals:
            terminal.draw(game.screen, game.player.rect)
        game.player.draw(game.screen)

        game.ui_manager.draw_gameplay_ui(game.tiempo_restante, game.terminals)

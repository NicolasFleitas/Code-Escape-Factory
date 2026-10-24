"""Playing (exploration) scene."""

import pygame

from src.game_state import GameState
from src.scenes.base import BaseScene


class PlayingScene(BaseScene):
    """Free movement, terminal interaction, and the countdown timer."""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for terminal in self.game.terminals:
                    if terminal.is_player_near(self.game.player.rect):
                        self.game.active_terminal = terminal
                        self.game.puzzle.set_puzzle(terminal.task_id)
                        self.game.change_state(GameState.PROGRAMMING)
                        break
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state(GameState.PAUSED)
                self.game.pausa_start_time = pygame.time.get_ticks()
                pygame.mixer.music.pause()

    def update(self, dt):
        game = self.game
        self._update_timer()
        self._update_audio_sync()
        if game.state is not GameState.PLAYING:
            return

        game.player.update(game.map_manager.walls)

        if not game.puerta_abierta:
            if game.player.rect.colliderect(game.door_rect):
                game.player.rect.right = game.door_rect.left
        else:
            if game.player.rect.colliderect(game.door_rect):
                game.change_state(GameState.WON)
                audio = game.audio_manager
                if audio.victoria_sound and not game.victoria_sound_played:
                    pygame.mixer.music.pause()
                    audio.victoria_sound.play()
                    game.victoria_sound_played = True
                    game.victoria_sound_start_time = pygame.time.get_ticks()

    def draw(self):
        self._draw_world()
        self._draw_gameplay()

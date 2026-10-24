"""Game loop and scene router for Code Escape: Factory Reset."""

import pygame

from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TIEMPO_LIMITE, TILE_SIZE,
)

from src.player import Player
from src.terminal import Terminal
from src.puzzle_manager import PuzzleManager
from src.map_manager import MapManager
from src.audio_manager import AudioManager
from src.ui_manager import UIManager
from src.character_selector import CharacterSelector

from src.game_state import GameState
from src.scenes.character_select import CharacterSelectScene
from src.scenes.game_over import GameOverScene
from src.scenes.menu import MenuScene
from src.scenes.paused import PausedScene
from src.scenes.playing import PlayingScene
from src.scenes.programming import ProgrammingScene


class Game:
    """Owns pygame setup, the shared session state, and the scene router.

    Game is only the loop and the router (CONTRIBUTING section 6): the
    behavior of each state lives in its scene, under src/scenes/.
    """

    def __init__(self):
        self._init_pygame()

        # Managers
        self.audio_manager = AudioManager()
        self.audio_manager.setup()

        self.ui_manager = UIManager(self.screen)
        self.map_manager = MapManager()
        self.puzzle = PuzzleManager()
        self.character_selector = CharacterSelector(self.screen)

        self._setup_entities()
        self._setup_session_state()
        self._setup_scenes()
        self.change_state(GameState.MENU)
        self.running = True

    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED
        )
        pygame.display.set_caption("Code Escape: Factory Reset")
        self.clock = pygame.time.Clock()

    def _setup_entities(self):
        self.player = Player(
            x=self.map_manager.player_spawn[0], y=self.map_manager.player_spawn[1]
        )
        self.terminals = [
            Terminal(pos[0], pos[1], task_id=i + 1)
            for i, pos in enumerate(self.map_manager.terminals)
        ]
        self.active_terminal = None
        self.door_rect = pygame.Rect(
            self.map_manager.door_pos[0], self.map_manager.door_pos[1],
            TILE_SIZE, TILE_SIZE,
        )
        self.puerta_abierta = False

    def _setup_session_state(self):
        """Reset the per-run state shared by the scenes."""
        self.tiempo_restante = TIEMPO_LIMITE
        self.inicio_ticks = None
        self.pausa_start_time = 0

        # Sound played flags: single owner, Game (CONTRIBUTING section 6).
        self.victoria_sound_played = False
        self.victoria_sound_start_time = None
        self.derrota_sound_played = False
        self.derrota_sound_start_time = None
        self.alarma_10s_played = False
        self.alarma_5s_played = False

    def _setup_scenes(self):
        self.scenes = {
            GameState.MENU: MenuScene(self),
            GameState.CHARACTER_SELECT: CharacterSelectScene(self),
            GameState.PLAYING: PlayingScene(self),
            GameState.PROGRAMMING: ProgrammingScene(self),
            GameState.PAUSED: PausedScene(self),
            GameState.WON: GameOverScene(self, GameState.WON),
            GameState.LOST: GameOverScene(self, GameState.LOST),
        }

    # --- Router ---

    def change_state(self, state):
        self.state = state
        self.scene = self.scenes[state]

    def quit(self):
        """Request the main loop to stop (scenes never call sys.exit)."""
        self.running = False

    def reset_game(self):
        """Reset the session for a new run; the caller picks the state."""
        self._setup_entities()
        self._setup_session_state()
        self._setup_scenes()
        pygame.mixer.music.unpause()

        # Reset the character selector so selection starts fresh.
        self.character_selector.en_menu = True
        self.character_selector.indice_seleccionado = 0
        self.character_selector.personaje_elegido = None
        self.character_selector.imagen_elegida = None

    # --- Main loop ---

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    break
                self.scene.handle_event(event)
                if not self.running:
                    break

            if not self.running:
                break

            self.scene.update(dt)
            self.scene.draw()
            pygame.display.flip()

        pygame.quit()

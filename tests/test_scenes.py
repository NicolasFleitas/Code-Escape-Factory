"""Tests for the scene-based state machine (GameState + scenes).

Every test runs headless: scenes only need ``pygame.Rect`` and synthetic
events, so no display or mixer is initialized. Time and mixer calls are
monkeypatched to keep the tests deterministic.
"""

from types import SimpleNamespace

import pygame

from src.game_state import GameState
from src.settings import TIEMPO_LIMITE
from src.scenes.character_select import CharacterSelectScene
from src.scenes.game_over import GameOverScene
from src.scenes.menu import MenuScene
from src.scenes.paused import PausedScene
from src.scenes.playing import PlayingScene
from src.scenes.programming import ProgrammingScene


def key_event(key):
    """Build a synthetic KEYDOWN event (works without pygame.init)."""
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def click_event(x, y):
    """Build a synthetic left-click event at (x, y)."""
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(x, y), button=1)


class FakeSound:
    def __init__(self):
        self.played = 0

    def play(self):
        self.played += 1


class FakeMusic:
    def __init__(self):
        self.paused = 0
        self.unpaused = 0

    def pause(self):
        self.paused += 1

    def unpause(self):
        self.unpaused += 1


class FakeAudioManager:
    def __init__(self):
        self.victoria_sound = None
        self.derrota_sound = None
        self.alarma_sound = None

    def check_sound_completion(self, start_time, sound):
        return False


class FakePlayer:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.load_calls = []
        self.update_calls = []

    def load_sprites(self, character_id=1):
        self.load_calls.append(character_id)

    def update(self, dt, direction=(0, 0), walls=None):
        self.update_calls.append((dt, direction, walls))

    def block_left_of(self, blocker):
        self.rect.right = blocker.left


class FakeInput:
    """Stands in for the input adapter: fixed direction, zero pygame access."""

    def __init__(self, direction=(0, 0)):
        self.direction = direction
        self.calls = 0

    def movement_direction(self):
        self.calls += 1
        return self.direction


class FakeTerminal:
    def __init__(self, task_id, near=False, solved=False):
        self.task_id = task_id
        self.solved = solved
        self.near = near

    def is_player_near(self, player_rect):
        return self.near


class FakePuzzle:
    def __init__(self):
        self.set_calls = []
        self.result = None

    def set_puzzle(self, task_id):
        self.set_calls.append(task_id)

    def handle_event(self, event):
        return self.result


class FakeSelector:
    def __init__(self):
        self.indice_seleccionado = 0
        self.completed = False

    def handle_event(self, event):
        return self.completed


class FakeScreen:
    def __init__(self):
        self.filled = 0

    def fill(self, color):
        self.filled += 1

    def blit(self, source, dest):
        pass


class FakeUIManager:
    def __init__(self):
        self.end_screen_states = []

    def draw_end_screen(self, game_state, **kwargs):
        self.end_screen_states.append(game_state)


class FakeGame:
    """Stands in for Game: records routing decisions, owns fake session state."""

    def __init__(self):
        # A scene only updates while its state is routed (Game.change_state
        # sets this before any scene runs).
        self.state = GameState.PLAYING
        self.transitions = []
        self.quit_called = False
        self.reset_calls = 0

        self.audio_manager = FakeAudioManager()
        self.player = FakePlayer()
        self.input = FakeInput()
        self.map_manager = SimpleNamespace(walls=[], draw=lambda screen: None)
        self.puzzle = FakePuzzle()
        self.character_selector = FakeSelector()
        self.ui_manager = FakeUIManager()
        self.screen = FakeScreen()

        self.terminals = []
        self.active_terminal = None
        self.door_rect = pygame.Rect(0, 0, 64, 64)
        self.puerta_abierta = False
        self.tiempo_restante = TIEMPO_LIMITE
        self.inicio_ticks = None
        self.pausa_start_time = 0

        self.victoria_sound_played = False
        self.victoria_sound_start_time = None
        self.derrota_sound_played = False
        self.derrota_sound_start_time = None
        self.alarma_10s_played = False
        self.alarma_5s_played = False

    def change_state(self, state):
        self.transitions.append(state)
        self.state = state

    def quit(self):
        self.quit_called = True

    def reset_game(self):
        self.reset_calls += 1


def make_game_with_music(monkeypatch):
    game = FakeGame()
    music = FakeMusic()
    monkeypatch.setattr(pygame.mixer, "music", music)
    return game, music


# --- GameState enum ---


def test_game_state_covers_every_scene():
    assert {state.name for state in GameState} == {
        "MENU",
        "CHARACTER_SELECT",
        "PLAYING",
        "PROGRAMMING",
        "PAUSED",
        "WON",
        "LOST",
    }


# --- MenuScene ---


def test_menu_navigation_wraps_around():
    scene = MenuScene(FakeGame())

    scene.handle_event(key_event(pygame.K_DOWN))
    assert scene.selected_option == 1
    scene.handle_event(key_event(pygame.K_DOWN))
    assert scene.selected_option == 0
    scene.handle_event(key_event(pygame.K_UP))
    assert scene.selected_option == 1


def test_menu_start_goes_to_character_select():
    game = FakeGame()
    scene = MenuScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.transitions == [GameState.CHARACTER_SELECT]
    assert not game.quit_called


def test_menu_exit_quits_the_game():
    game = FakeGame()
    scene = MenuScene(game)

    scene.handle_event(key_event(pygame.K_DOWN))
    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.quit_called
    assert game.transitions == []


def test_menu_mouse_click_starts_game():
    game = FakeGame()
    scene = MenuScene(game)

    scene.handle_event(click_event(*scene.botones_rects[0].center))

    assert game.transitions == [GameState.CHARACTER_SELECT]


# --- CharacterSelectScene ---


def test_character_select_completes_selection_and_starts_timer(monkeypatch):
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 1234)
    game = FakeGame()
    game.character_selector.completed = True
    game.character_selector.indice_seleccionado = 2
    scene = CharacterSelectScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.player.load_calls == [3]
    assert game.inicio_ticks == 1234
    assert game.transitions == [GameState.PLAYING]


def test_character_select_pending_selection_does_not_transition(monkeypatch):
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 1234)
    game = FakeGame()
    scene = CharacterSelectScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.transitions == []
    assert game.inicio_ticks is None
    assert game.player.load_calls == []


# --- PlayingScene: events ---


def test_playing_opens_near_terminal():
    game = FakeGame()
    terminal = FakeTerminal(task_id=1, near=True)
    game.terminals = [terminal]
    scene = PlayingScene(game)

    scene.handle_event(key_event(pygame.K_e))

    assert game.active_terminal is terminal
    assert game.puzzle.set_calls == [1]
    assert game.transitions == [GameState.PROGRAMMING]


def test_playing_ignores_far_terminals():
    game = FakeGame()
    game.terminals = [FakeTerminal(task_id=1, near=False)]
    scene = PlayingScene(game)

    scene.handle_event(key_event(pygame.K_e))

    assert game.active_terminal is None
    assert game.puzzle.set_calls == []
    assert game.transitions == []


def test_playing_escape_pauses_and_pauses_music(monkeypatch):
    game, music = make_game_with_music(monkeypatch)
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 500)
    scene = PlayingScene(game)

    scene.handle_event(key_event(pygame.K_ESCAPE))

    assert game.transitions == [GameState.PAUSED]
    assert game.pausa_start_time == 500
    assert music.paused == 1


# --- PlayingScene: update ---


def test_playing_timer_expires_and_loses(monkeypatch):
    game, music = make_game_with_music(monkeypatch)
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 60000)
    game.inicio_ticks = 0
    derrota = FakeSound()
    game.audio_manager.derrota_sound = derrota
    scene = PlayingScene(game)

    scene.update(0)

    assert game.transitions == [GameState.LOST]
    assert game.derrota_sound_played
    assert game.derrota_sound_start_time == 60000
    assert derrota.played == 1
    assert music.paused == 1
    # Movement must not run after the state changed mid-update.
    assert game.player.update_calls == []


def test_playing_timer_does_not_run_before_the_run_starts():
    game = FakeGame()
    scene = PlayingScene(game)

    scene.update(0)

    assert game.transitions == []
    assert game.tiempo_restante == TIEMPO_LIMITE
    assert game.player.update_calls == [(0, (0, 0), game.map_manager.walls)]


def test_playing_passes_delta_time_and_direction_to_the_player():
    game = FakeGame()
    game.input.direction = (1, -1)
    scene = PlayingScene(game)

    scene.update(0.25)

    assert game.input.calls == 1
    assert game.player.update_calls == [(0.25, (1, -1), game.map_manager.walls)]


def test_playing_alarm_at_10s_plays_once(monkeypatch):
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 50000)
    game = FakeGame()
    game.inicio_ticks = 0
    alarma = FakeSound()
    game.audio_manager.alarma_sound = alarma
    scene = PlayingScene(game)

    scene.update(0)
    assert game.alarma_10s_played
    assert alarma.played == 1

    scene.update(0)
    assert alarma.played == 1


def test_playing_wins_through_the_open_door(monkeypatch):
    game, music = make_game_with_music(monkeypatch)
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 777)
    game.puerta_abierta = True
    game.player.rect.topleft = (0, 0)
    victoria = FakeSound()
    game.audio_manager.victoria_sound = victoria
    scene = PlayingScene(game)

    scene.update(0)

    assert game.transitions == [GameState.WON]
    assert game.victoria_sound_played
    assert game.victoria_sound_start_time == 777
    assert victoria.played == 1
    assert music.paused == 1


def test_playing_closed_door_pushes_player_back():
    game = FakeGame()
    game.player.rect.topleft = (0, 0)
    scene = PlayingScene(game)

    scene.update(0)

    assert game.player.rect.right == game.door_rect.left
    assert game.transitions == []


# --- ProgrammingScene ---


def test_programming_solved_opens_door_when_all_terminals_solved():
    game = FakeGame()
    terminal = FakeTerminal(task_id=1)
    game.active_terminal = terminal
    game.terminals = [terminal]
    game.puzzle.result = "SOLVED"
    scene = ProgrammingScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert terminal.solved
    assert game.puerta_abierta


def test_programming_solved_keeps_door_closed_while_others_pending():
    game = FakeGame()
    active = FakeTerminal(task_id=1)
    other = FakeTerminal(task_id=2)
    game.active_terminal = active
    game.terminals = [active, other]
    game.puzzle.result = "SOLVED"
    scene = ProgrammingScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert active.solved
    assert not game.puerta_abierta


def test_programming_escape_returns_to_playing():
    game = FakeGame()
    scene = ProgrammingScene(game)

    scene.handle_event(key_event(pygame.K_ESCAPE))

    assert game.transitions == [GameState.PLAYING]


def test_programming_wrong_answer_changes_nothing():
    game = FakeGame()
    terminal = FakeTerminal(task_id=1)
    game.active_terminal = terminal
    game.terminals = [terminal]
    game.puzzle.result = None
    scene = ProgrammingScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert not terminal.solved
    assert not game.puerta_abierta
    assert game.transitions == []


# --- PausedScene ---


def test_pause_continue_resumes_and_shifts_the_timer(monkeypatch):
    game, music = make_game_with_music(monkeypatch)
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 55000)
    game.inicio_ticks = 5000
    game.pausa_start_time = 51000
    scene = PausedScene(game)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.inicio_ticks == 9000
    assert game.transitions == [GameState.PLAYING]
    assert music.unpaused == 1


def test_pause_escape_resumes(monkeypatch):
    game, music = make_game_with_music(monkeypatch)
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 55000)
    game.inicio_ticks = 5000
    game.pausa_start_time = 51000
    scene = PausedScene(game)

    scene.handle_event(key_event(pygame.K_ESCAPE))

    assert game.inicio_ticks == 9000
    assert game.transitions == [GameState.PLAYING]
    assert music.unpaused == 1


def test_pause_exit_resets_and_returns_to_menu():
    game = FakeGame()
    scene = PausedScene(game)

    scene.handle_event(key_event(pygame.K_DOWN))
    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.reset_calls == 1
    assert game.transitions == [GameState.MENU]


# --- GameOverScene ---


def test_game_over_restart_resets_and_goes_to_character_select():
    game = FakeGame()
    scene = GameOverScene(game, GameState.LOST)

    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.reset_calls == 1
    assert game.transitions == [GameState.CHARACTER_SELECT]


def test_game_over_menu_option_returns_to_menu():
    game = FakeGame()
    scene = GameOverScene(game, GameState.WON)

    scene.handle_event(key_event(pygame.K_RIGHT))
    scene.handle_event(key_event(pygame.K_RETURN))

    assert game.reset_calls == 1
    assert game.transitions == [GameState.MENU]


def test_game_over_draw_passes_the_outcome_to_the_ui():
    game = FakeGame()
    scene = GameOverScene(game, GameState.WON)

    scene.draw()

    assert game.ui_manager.end_screen_states == [GameState.WON]
    assert game.screen.filled == 1

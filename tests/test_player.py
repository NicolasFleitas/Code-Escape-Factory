"""Tests for Player movement: delta time and injected direction.

The Player never reads the keyboard; the direction arrives as a parameter.
Movement is expressed in pixels per second and scaled by dt, so the game
speed does not depend on the frame rate.
"""

import math

import pygame
import pytest

from src.player import Player
from src.settings import PLAYER_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH


def make_player(monkeypatch, x=100, y=100):
    """Player with sprite loading stubbed out (no display needed)."""
    monkeypatch.setattr(Player, "load_sprites", lambda self, character_id=1: None)
    return Player(x=x, y=y)


@pytest.fixture
def player(monkeypatch):
    return make_player(monkeypatch)


def test_update_moves_speed_times_dt(player):
    player.update(0.5, (1, 0))

    assert player.rect.x == pytest.approx(100 + PLAYER_SPEED * 0.5)


def test_movement_is_frame_rate_independent(player, monkeypatch):
    smooth = make_player(monkeypatch)
    player.update(1.0, (1, 0))
    for _ in range(60):
        smooth.update(1 / 60, (1, 0))

    assert smooth.rect.x == pytest.approx(player.rect.x, abs=1)


def test_small_steps_accumulate_without_losing_pixels(player):
    for _ in range(60):
        player.update(1 / 60, (1, 0))

    assert player.rect.x == pytest.approx(100 + PLAYER_SPEED, abs=1)


def test_diagonal_is_not_faster_than_straight(player, monkeypatch):
    diagonal = make_player(monkeypatch)

    player.update(1.0, (1, 0))
    diagonal.update(1.0, (1, 1))

    straight_distance = player.rect.x - 100
    diagonal_distance = math.hypot(diagonal.rect.x - 100, diagonal.rect.y - 100)
    assert diagonal_distance == pytest.approx(straight_distance, abs=1)


def test_diagonal_keeps_its_speed_at_sixty_fps(player, monkeypatch):
    diagonal = make_player(monkeypatch)

    for _ in range(60):
        player.update(1 / 60, (1, 0))
        diagonal.update(1 / 60, (1, 1))

    straight_distance = player.rect.x - 100
    diagonal_distance = math.hypot(diagonal.rect.x - 100, diagonal.rect.y - 100)
    assert diagonal_distance == pytest.approx(straight_distance, abs=2)


def test_update_never_reads_the_keyboard(player, monkeypatch):
    def forbidden():
        raise AssertionError("Player.update must not read pygame.key")

    monkeypatch.setattr(pygame.key, "get_pressed", forbidden)

    player.update(0.016, (1, 0))


def test_neutral_direction_keeps_the_player_still_and_facing(player):
    player.direction = "frente"

    player.update(0.5, (0, 0))

    assert player.rect.topleft == (100, 100)
    assert player.direction == "frente"


def test_default_direction_is_neutral(player):
    player.update(0.5)

    assert player.rect.topleft == (100, 100)


def test_facing_prefers_the_horizontal_axis(player):
    player.update(0.016, (-1, -1))
    assert player.direction == "izquierda"

    player.update(0.016, (1, 0))
    assert player.direction == "derecha"


def test_vertical_facing_only_when_no_horizontal_input(player):
    player.update(0.016, (0, -1))
    assert player.direction == "espalda"

    player.update(0.016, (0, 1))
    assert player.direction == "frente"


def test_walls_block_horizontal_movement(player):
    wall = pygame.Rect(150, 100, 64, 64)

    player.update(1.0, (1, 0), [wall])

    assert player.rect.right == wall.left


def test_walls_block_vertical_movement(player):
    wall = pygame.Rect(100, 150, 64, 64)

    player.update(1.0, (0, 1), [wall])

    assert player.rect.bottom == wall.top


def test_movement_is_clamped_to_the_screen(player):
    player.update(10.0, (1, 0))

    assert player.rect.right == SCREEN_WIDTH


def test_upward_movement_is_clamped_to_the_screen(player):
    player.update(10.0, (0, -1))

    assert player.rect.top == 0
    assert player.rect.bottom <= SCREEN_HEIGHT

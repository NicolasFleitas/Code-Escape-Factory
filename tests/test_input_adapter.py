"""Tests for the keyboard input adapter.

The adapter is the only place allowed to read ``pygame.key.get_pressed``:
it turns the keyboard state into a movement direction that entities consume.
"""

import pygame

from src.input_adapter import InputAdapter, read_movement_direction


class FakeKeyState:
    """Stands in for the sequence returned by ``pygame.key.get_pressed``."""

    def __init__(self, *pressed_keys):
        self._down = set(pressed_keys)

    def __getitem__(self, key):
        return key in self._down


def test_neutral_when_no_key_is_pressed():
    assert read_movement_direction(FakeKeyState()) == (0, 0)


def test_arrow_keys_map_to_axes():
    assert read_movement_direction(FakeKeyState(pygame.K_LEFT)) == (-1, 0)
    assert read_movement_direction(FakeKeyState(pygame.K_RIGHT)) == (1, 0)
    assert read_movement_direction(FakeKeyState(pygame.K_UP)) == (0, -1)
    assert read_movement_direction(FakeKeyState(pygame.K_DOWN)) == (0, 1)


def test_wasd_keys_are_aliases_for_the_arrows():
    assert read_movement_direction(FakeKeyState(pygame.K_a)) == (-1, 0)
    assert read_movement_direction(FakeKeyState(pygame.K_d)) == (1, 0)
    assert read_movement_direction(FakeKeyState(pygame.K_w)) == (0, -1)
    assert read_movement_direction(FakeKeyState(pygame.K_s)) == (0, 1)


def test_opposite_keys_cancel_on_the_same_axis():
    state = FakeKeyState(pygame.K_LEFT, pygame.K_RIGHT)

    assert read_movement_direction(state) == (0, 0)


def test_diagonal_combines_both_axes():
    state = FakeKeyState(pygame.K_LEFT, pygame.K_UP)

    assert read_movement_direction(state) == (-1, -1)


def test_arrow_and_wasd_aliases_cancel_too():
    state = FakeKeyState(pygame.K_a, pygame.K_RIGHT)

    assert read_movement_direction(state) == (0, 0)


def test_adapter_reads_the_live_keyboard_state(monkeypatch):
    state = FakeKeyState(pygame.K_RIGHT)
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: state)

    assert InputAdapter().movement_direction() == (1, 0)

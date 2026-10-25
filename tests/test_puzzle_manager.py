"""Tests for the puzzle session wiring.

PuzzleManager keeps the input/UI state and delegates the verdict to the
validator the puzzle declares; the font and the error sound are stubbed so the
tests stay headless.
"""

import pygame
import pytest

from src.puzzle_manager import PuzzleManager


class FakeSound:
    def play(self):
        pass


@pytest.fixture
def manager(monkeypatch):
    monkeypatch.setattr(pygame.font, "SysFont", lambda *args, **kwargs: None)
    monkeypatch.setattr(pygame.mixer, "Sound", lambda *args, **kwargs: FakeSound())
    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 0)
    return PuzzleManager()


def type_text(manager, text):
    for char in text:
        event = pygame.event.Event(pygame.KEYDOWN, key=ord(char), unicode=char)
        manager.handle_event(event)


def press(manager, key):
    return manager.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, unicode=""))


def test_set_puzzle_builds_the_declared_validator(manager):
    manager.set_puzzle(2)

    type_text(manager, "energia=100")

    assert press(manager, pygame.K_RETURN) == "SOLVED"
    assert manager.is_solved


def test_wrong_answer_is_not_solved(manager):
    manager.set_puzzle(2)

    type_text(manager, "energia = 50")

    assert press(manager, pygame.K_RETURN) is None
    assert not manager.is_solved
    assert manager.show_error


def test_no_puzzle_loaded_cannot_be_solved(manager):
    # Before set_puzzle there is no validator: RETURN must not unlock anything.
    assert press(manager, pygame.K_RETURN) is None
    assert not manager.is_solved

"""Keyboard input adapter.

This module is the only place that reads ``pygame.key``: it turns raw
keyboard state into game intents (a movement direction) that entities
consume, so gameplay code stays testable without a display (CONTRIBUTING
section 6: entities never read the keyboard).
"""

import pygame

NEUTRAL = (0, 0)

_LEFT_KEYS = (pygame.K_a, pygame.K_LEFT)
_RIGHT_KEYS = (pygame.K_d, pygame.K_RIGHT)
_UP_KEYS = (pygame.K_w, pygame.K_UP)
_DOWN_KEYS = (pygame.K_s, pygame.K_DOWN)


def _any_pressed(keys, candidates):
    return any(keys[key] for key in candidates)


def read_movement_direction(keys):
    """Map a key state (``pygame.key.get_pressed``-like) to ``(dx, dy)``.

    Each axis is -1, 0 or 1. Pressing both directions of an axis cancels it,
    so the adapter never depends on which key was pressed last.
    """
    dx = int(_any_pressed(keys, _RIGHT_KEYS)) - int(_any_pressed(keys, _LEFT_KEYS))
    dy = int(_any_pressed(keys, _DOWN_KEYS)) - int(_any_pressed(keys, _UP_KEYS))
    return dx, dy


class InputAdapter:
    """Reads the live keyboard and exposes game intents."""

    def movement_direction(self):
        """Current movement direction from the keyboard, as ``(dx, dy)``."""
        return read_movement_direction(pygame.key.get_pressed())

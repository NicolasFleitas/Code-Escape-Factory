"""Game states routed by the scene machine."""

from enum import Enum, auto


class GameState(Enum):
    """Every state of the game; each one routes to exactly one scene."""

    MENU = auto()
    CHARACTER_SELECT = auto()
    PLAYING = auto()
    PROGRAMMING = auto()
    PAUSED = auto()
    WON = auto()
    LOST = auto()

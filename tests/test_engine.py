"""Tests for the game loop's delta time handling."""

from src.engine import clamp_delta_time
from src.settings import MAX_DELTA_TIME


def test_short_frames_keep_their_delta():
    assert clamp_delta_time(0.016) == 0.016


def test_long_stall_is_capped():
    assert clamp_delta_time(2.0) == MAX_DELTA_TIME

"""Tests for the map renderer: tiles, draw order and the door overlay.

The renderer is the only map module that touches pygame surfaces, and it
never needs a window: surfaces and tiles load headless.
"""

import json

import pytest

from src.map_loader import DEFAULT_MAP_PATH, load_map
from src.map_renderer import MapRenderer
from src.settings import TILE_SIZE


class RecordingScreen:
    def __init__(self):
        self.blits = []

    def blit(self, source, dest):
        self.blits.append((source, dest))


@pytest.fixture
def map_data():
    return load_map(DEFAULT_MAP_PATH)


@pytest.fixture
def renderer(map_data):
    return MapRenderer(map_data)


def write_map(tmp_path, data):
    path = tmp_path / "map.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_loads_a_tile_for_every_legend_image(renderer, map_data):
    expected = {
        symbol for symbol, spec in map_data.legend.items() if spec.image is not None
    }

    assert set(renderer.tiles) == expected


def test_tiles_are_scaled_to_the_tile_size(renderer):
    assert all(
        tile.get_size() == (TILE_SIZE, TILE_SIZE) for tile in renderer.tiles.values()
    )


def test_draw_blits_every_floor_then_every_object(renderer, map_data):
    screen = RecordingScreen()

    renderer.draw(screen)

    floor_positions = [
        (column * TILE_SIZE, row * TILE_SIZE)
        for row in range(map_data.rows)
        for column in range(map_data.columns)
    ]
    object_positions = [
        (column * TILE_SIZE, row * TILE_SIZE)
        for row, symbols in enumerate(map_data.objects)
        for column, symbol in enumerate(symbols)
        if map_data.legend[symbol].image is not None
    ]
    # Floors go down first so translucent objects (desks, terminals) sit on top.
    assert [dest for _, dest in screen.blits] == floor_positions + object_positions
    assert all(source in renderer.tiles.values() for source, _ in screen.blits)


def test_missing_tile_falls_back_to_magenta(tmp_path):
    data = {
        "floor": ["..."],
        "objects": ["PTD"],
        "legend": {
            ".": {"image": "does_not_exist.png"},
            "P": {"spawn": True},
            "T": {"image": "terminal.png", "terminal": True},
            "D": {"image": "door.png", "door": True},
        },
        "door_open_image": "door_open.png",
    }

    renderer = MapRenderer(load_map(write_map(tmp_path, data)))

    assert renderer.tiles["."].get_at((0, 0)) == (255, 0, 255, 255)


def test_door_tile_switches_with_the_door_state(renderer):
    closed = renderer.door_tile(is_open=False)
    opened = renderer.door_tile(is_open=True)

    assert closed is renderer.tiles["D"]
    assert opened is not closed
    assert opened.get_size() == (TILE_SIZE, TILE_SIZE)

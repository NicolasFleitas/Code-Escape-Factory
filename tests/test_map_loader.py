"""Tests for the JSON map data format and its loader.

Maps are data (CONTRIBUTING section 6): the layout, the objects and the
tile legend live in ``src/assets/maps/*.json`` and the loader turns them
into a ``MapData`` value with no display or window involved.
"""

import json

import pygame
import pytest

from src.map_loader import DEFAULT_MAP_PATH, MapDataError, load_map
from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE


def minimal_map():
    """Smallest valid map: spawn, terminal, door and one solid wall."""
    return {
        "name": "test-room",
        "floor": ["..", ".."],
        "objects": ["PT", "WD"],
        "legend": {
            ".": {"image": "floor_room1.png"},
            "P": {"spawn": True},
            "W": {"image": "wall.png", "solid": True},
            "T": {"image": "terminal.png", "terminal": True},
            "D": {"image": "door.png", "door": True},
        },
        "door_open_image": "door_open.png",
    }


def write_map(tmp_path, data):
    path = tmp_path / "map.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# --- Factory map ---


def test_loads_the_factory_map():
    map_data = load_map(DEFAULT_MAP_PATH)

    assert map_data.name == "factory"
    assert map_data.rows == 12
    assert map_data.columns == 20
    assert len(map_data.floor) == map_data.rows
    assert all(len(row) == map_data.columns for row in map_data.objects)


def test_map_fits_the_screen():
    """Resolves the old 768 (12 rows) vs 720 mismatch."""
    map_data = load_map(DEFAULT_MAP_PATH)

    assert map_data.pixel_width == map_data.columns * TILE_SIZE == SCREEN_WIDTH
    assert map_data.pixel_height == map_data.rows * TILE_SIZE == SCREEN_HEIGHT


def test_derives_spawn_door_and_terminals_in_pixels():
    map_data = load_map(DEFAULT_MAP_PATH)

    assert map_data.player_spawn == (9 * TILE_SIZE, 5 * TILE_SIZE)
    assert map_data.door_pos == (19 * TILE_SIZE, 5 * TILE_SIZE)
    assert map_data.terminals == (
        (8 * TILE_SIZE, 2 * TILE_SIZE),
        (10 * TILE_SIZE, 2 * TILE_SIZE),
        (8 * TILE_SIZE, 8 * TILE_SIZE),
        (10 * TILE_SIZE, 10 * TILE_SIZE),
    )


def test_solid_objects_become_walls():
    map_data = load_map(DEFAULT_MAP_PATH)

    # 97 walls plus the solid furniture (desks, machines, plants, ...).
    assert len(map_data.walls) == 110
    assert pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE) in map_data.walls
    # Non-solid objects keep the player able to walk over them.
    chair = pygame.Rect(8 * TILE_SIZE, 1 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    assert chair not in map_data.walls


def test_floor_under_objects_is_explicit_data():
    map_data = load_map(DEFAULT_MAP_PATH)

    # The tile under the desk at (5, 1) belongs to office 1, not to a
    # coordinate heuristic: the floor layer says so.
    assert map_data.floor[1][5] == "."
    # The corridor tile under the player spawn.
    assert map_data.floor[5][9] == "-"


# --- Validation ---


def test_symbols_outside_the_legend_are_rejected(tmp_path):
    data = minimal_map()
    data["objects"] = ["PT", "W?"]

    with pytest.raises(MapDataError, match=r"\?"):
        load_map(write_map(tmp_path, data))


def test_ragged_layers_are_rejected(tmp_path):
    data = minimal_map()
    data["floor"] = ["..", "..."]

    with pytest.raises(MapDataError, match="rectangular"):
        load_map(write_map(tmp_path, data))


def test_layers_must_share_their_dimensions(tmp_path):
    data = minimal_map()
    data["objects"] = ["PT"]

    with pytest.raises(MapDataError, match="same dimensions"):
        load_map(write_map(tmp_path, data))


def test_requires_exactly_one_spawn(tmp_path):
    data = minimal_map()
    data["objects"] = ["..", "WD"]

    with pytest.raises(MapDataError, match="spawn"):
        load_map(write_map(tmp_path, data))

    duplicated = minimal_map()
    duplicated["objects"] = ["PP", "WD"]
    with pytest.raises(MapDataError, match="spawn"):
        load_map(write_map(tmp_path, duplicated))


def test_requires_exactly_one_door(tmp_path):
    data = minimal_map()
    data["objects"] = ["PT", "W."]

    with pytest.raises(MapDataError, match="door"):
        load_map(write_map(tmp_path, data))


def test_requires_at_least_one_terminal(tmp_path):
    data = minimal_map()
    data["objects"] = ["P.", "WD"]

    with pytest.raises(MapDataError, match="terminal"):
        load_map(write_map(tmp_path, data))


def test_floor_symbols_need_an_image(tmp_path):
    data = minimal_map()
    data["legend"]["."] = {}

    with pytest.raises(MapDataError, match="image"):
        load_map(write_map(tmp_path, data))


def test_door_needs_an_image(tmp_path):
    data = minimal_map()
    data["legend"]["D"] = {"door": True}

    with pytest.raises(MapDataError, match="door"):
        load_map(write_map(tmp_path, data))


def test_missing_required_section_is_rejected(tmp_path):
    data = minimal_map()
    del data["legend"]

    with pytest.raises(MapDataError, match="legend"):
        load_map(write_map(tmp_path, data))


def test_invalid_json_is_rejected(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(MapDataError, match="JSON"):
        load_map(path)

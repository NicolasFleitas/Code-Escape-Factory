"""Loads map layouts from JSON data files.

Maps are data, not code (CONTRIBUTING section 6): the layout, the
objects and the tile legend live in ``src/assets/maps/*.json``. This
module turns one of those files into a ``MapData`` value with collision
rects and entity positions; drawing lives in ``src/map_renderer.py``.

The loader is headless: it only builds ``pygame.Rect`` values, which do
not need a display.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pygame

from src.settings import TILE_SIZE

MAPS_DIR = Path(__file__).resolve().parent / "assets" / "maps"
DEFAULT_MAP_PATH = MAPS_DIR / "factory.json"


class MapDataError(ValueError):
    """Raised when a map file is missing, malformed or inconsistent."""


@dataclass(frozen=True)
class TileSpec:
    """One legend entry: how a map symbol is drawn and what it means."""

    image: str | None = None
    solid: bool = False
    terminal: bool = False
    door: bool = False
    spawn: bool = False


@dataclass(frozen=True)
class MapData:
    """A loaded map: two layers plus the entities derived from them."""

    name: str
    floor: tuple[str, ...]
    objects: tuple[str, ...]
    legend: dict[str, TileSpec]
    door_open_image: str
    tile_size: int
    player_spawn: tuple[int, int]
    terminals: tuple[tuple[int, int], ...]
    door_pos: tuple[int, int]
    walls: tuple[pygame.Rect, ...]

    @property
    def rows(self) -> int:
        return len(self.objects)

    @property
    def columns(self) -> int:
        return len(self.objects[0])

    @property
    def pixel_width(self) -> int:
        return self.columns * self.tile_size

    @property
    def pixel_height(self) -> int:
        return self.rows * self.tile_size


def load_map(path=DEFAULT_MAP_PATH) -> MapData:
    """Read and validate a map file, returning its ``MapData``."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise MapDataError(f"cannot read map file {path}: {error}") from error

    try:
        raw = json.loads(text)
    except json.JSONDecodeError as error:
        raise MapDataError(f"invalid JSON in {path}: {error}") from error

    if not isinstance(raw, dict):
        raise MapDataError(f"{path}: the map must be a JSON object")

    return _build_map(raw, path)


def _build_map(raw, path):
    name = raw.get("name", path.stem)
    legend = _parse_legend(raw, path)
    floor = _parse_layer(raw, "floor", path)
    objects = _parse_layer(raw, "objects", path)

    if (len(floor[0]), len(floor)) != (len(objects[0]), len(objects)):
        raise MapDataError(
            f"{path}: floor and objects layers must have the same dimensions"
        )

    used_symbols = {symbol for row in floor + objects for symbol in row}
    unknown = sorted(used_symbols - legend.keys())
    if unknown:
        raise MapDataError(
            f"{path}: symbols outside the legend: {' '.join(unknown)}"
        )

    for row_index, row in enumerate(floor):
        for column, symbol in enumerate(row):
            spec = legend[symbol]
            if any((spec.solid, spec.terminal, spec.door, spec.spawn)):
                raise MapDataError(
                    f"{path}: floor cell ({column}, {row_index}) uses the "
                    f"object symbol '{symbol}'"
                )
            if spec.image is None:
                raise MapDataError(
                    f"{path}: floor symbol '{symbol}' needs an image"
                )

    door_open_image = raw.get("door_open_image")
    if not isinstance(door_open_image, str) or not door_open_image:
        raise MapDataError(f"{path}: 'door_open_image' must be a file name")

    walls = []
    spawns = []
    terminals = []
    doors = []
    for row_index, row in enumerate(objects):
        for column, symbol in enumerate(row):
            spec = legend[symbol]
            position = (column * TILE_SIZE, row_index * TILE_SIZE)
            if spec.solid:
                walls.append(pygame.Rect(position, (TILE_SIZE, TILE_SIZE)))
            if spec.spawn:
                spawns.append(position)
            if spec.terminal:
                terminals.append(position)
            if spec.door:
                if spec.image is None:
                    raise MapDataError(
                        f"{path}: door symbol '{symbol}' needs an image"
                    )
                doors.append(position)

    _require_single(path, "spawn", spawns)
    _require_single(path, "door", doors)
    if not terminals:
        raise MapDataError(f"{path}: the map needs at least one terminal")

    return MapData(
        name=name,
        floor=floor,
        objects=objects,
        legend=legend,
        door_open_image=door_open_image,
        tile_size=TILE_SIZE,
        player_spawn=spawns[0],
        terminals=tuple(terminals),
        door_pos=doors[0],
        walls=tuple(walls),
    )


def _parse_legend(raw, path):
    legend_raw = raw.get("legend")
    if not isinstance(legend_raw, dict) or not legend_raw:
        raise MapDataError(f"{path}: 'legend' must be a non-empty object")

    legend = {}
    for symbol, spec in legend_raw.items():
        if len(symbol) != 1:
            raise MapDataError(
                f"{path}: legend symbol '{symbol}' must be one character"
            )
        if not isinstance(spec, dict):
            raise MapDataError(
                f"{path}: legend entry '{symbol}' must be an object"
            )
        image = spec.get("image")
        if image is not None and not isinstance(image, str):
            raise MapDataError(
                f"{path}: legend entry '{symbol}' has a non-string image"
            )
        legend[symbol] = TileSpec(
            image=image,
            solid=bool(spec.get("solid", False)),
            terminal=bool(spec.get("terminal", False)),
            door=bool(spec.get("door", False)),
            spawn=bool(spec.get("spawn", False)),
        )
    return legend


def _parse_layer(raw, key, path):
    layer = raw.get(key)
    if not isinstance(layer, list) or not layer:
        raise MapDataError(f"{path}: '{key}' must be a non-empty list of rows")
    if not all(isinstance(row, str) and row for row in layer):
        raise MapDataError(f"{path}: '{key}' rows must be non-empty strings")

    width = len(layer[0])
    for row_index, row in enumerate(layer):
        if len(row) != width:
            raise MapDataError(
                f"{path}: '{key}' rows must be rectangular "
                f"(row 0 has {width} columns, row {row_index} has {len(row)})"
            )
    return tuple(layer)


def _require_single(path, role, positions):
    if len(positions) != 1:
        raise MapDataError(
            f"{path}: the map needs exactly one {role}, found {len(positions)}"
        )

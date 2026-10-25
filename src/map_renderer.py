"""Draws a loaded map onto a pygame surface.

The renderer is the only map module that knows about pygame surfaces and
tile files (CONTRIBUTING section 6). It reads a ``MapData`` produced by
``src/map_loader.py`` and never owns layout data.

It works headless: tiles load without a window, and display-format
conversion only happens when a display already exists.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pygame

from src.map_loader import MapData

ITEMS_DIR = Path(__file__).resolve().parent / "assets" / "items_mapa"
_MISSING_TILE_COLOR = (255, 0, 255)


class MapRenderer:
    def __init__(self, map_data: MapData, items_dir=ITEMS_DIR):
        self.map_data = map_data
        self.items_dir = Path(items_dir)
        self.tile_size = map_data.tile_size
        self.tiles = {
            symbol: self._load_tile(spec.image)
            for symbol, spec in map_data.legend.items()
            if spec.image is not None
        }
        self.door_open_tile = self._load_tile(map_data.door_open_image)

    def _load_tile(self, filename: str):
        path = self.items_dir / filename
        try:
            image = pygame.image.load(path)
        except (OSError, pygame.error):
            logging.warning("Map tile not found: %s", path)
            placeholder = pygame.Surface((self.tile_size, self.tile_size))
            placeholder.fill(_MISSING_TILE_COLOR)
            return placeholder

        if image.get_size() != (self.tile_size, self.tile_size):
            image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
        if pygame.display.get_surface() is not None:
            image = image.convert_alpha()
        return image

    def draw(self, screen):
        """Draw the floor layer first, then the objects on top of it."""
        data = self.map_data
        for row_index, row in enumerate(data.floor):
            for column, symbol in enumerate(row):
                screen.blit(
                    self.tiles[symbol],
                    (column * self.tile_size, row_index * self.tile_size),
                )

        for row_index, row in enumerate(data.objects):
            for column, symbol in enumerate(row):
                tile = self.tiles.get(symbol)
                if tile is not None:
                    screen.blit(
                        tile,
                        (column * self.tile_size, row_index * self.tile_size),
                    )

    def door_tile(self, is_open: bool):
        """The door sprite matching its current state."""
        return self.door_open_tile if is_open else self.tiles["D"]

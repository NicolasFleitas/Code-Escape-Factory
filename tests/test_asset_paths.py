"""Tests for the single asset-path module (CONTRIBUTING section 6).

Every asset location is resolved from ``src/asset_paths.py`` with
``pathlib`` and ``__file__``, so the game loads the same files no matter
which directory it is started from.
"""

from pathlib import Path

import pygame
import pytest

from src import asset_paths
from src.asset_paths import (
    ASSETS_DIR,
    AUDIO_DIR,
    CHARACTERS_DIR,
    ITEMS_DIR,
    MAPS_DIR,
    asset_path,
)


def test_assets_dir_is_resolved_from_the_module_file():
    expected = Path(asset_paths.__file__).resolve().parent / "assets"

    assert ASSETS_DIR == expected
    assert ASSETS_DIR.is_dir()


def test_asset_path_does_not_depend_on_the_working_directory(monkeypatch, tmp_path):
    expected = asset_path("audio", "ambiente.mp3")

    monkeypatch.chdir(tmp_path)

    assert asset_path("audio", "ambiente.mp3") == expected
    assert expected.is_file()


@pytest.mark.parametrize(
    "directory",
    [AUDIO_DIR, CHARACTERS_DIR, ITEMS_DIR, MAPS_DIR],
    ids=["audio", "characters", "items", "maps"],
)
def test_declared_asset_directories_exist(directory):
    assert directory.is_dir()


def test_pygame_loads_an_asset_through_the_shared_module():
    image = pygame.image.load(asset_path("items_mapa", "wall.png"))

    assert image.get_size() == (64, 64)


def test_map_modules_take_their_directories_from_the_shared_module():
    from src import map_loader, map_renderer

    assert map_loader.MAPS_DIR == MAPS_DIR
    assert map_loader.DEFAULT_MAP_PATH == MAPS_DIR / "factory.json"
    assert map_renderer.ITEMS_DIR == ITEMS_DIR


def test_no_module_builds_asset_paths_from_the_working_directory():
    source_root = Path(asset_paths.__file__).resolve().parent

    offenders = [
        path.relative_to(source_root).as_posix()
        for path in sorted(source_root.rglob("*.py"))
        if 'os.path.join("src", "assets"' in path.read_text(encoding="utf-8")
    ]

    assert offenders == []

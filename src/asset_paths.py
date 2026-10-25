"""Single source of truth for asset locations (CONTRIBUTING section 6).

Paths are resolved from this module's own file with ``pathlib``, so the
game finds its assets no matter which directory it is started from. No
other module may build an asset path from the process working directory.
"""

from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
CHARACTERS_DIR = ASSETS_DIR / "personajes"
ITEMS_DIR = ASSETS_DIR / "items_mapa"
MAPS_DIR = ASSETS_DIR / "maps"


def asset_path(*parts: str) -> Path:
    """Return the absolute path of an asset inside ``src/assets``."""
    return ASSETS_DIR.joinpath(*parts)

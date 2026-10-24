from src import settings


def test_colores_son_rgb_validos():
    colores = {
        nombre: valor
        for nombre, valor in vars(settings).items()
        if nombre.startswith("COLOR_")
    }

    assert colores
    for nombre, valor in colores.items():
        assert isinstance(valor, tuple), f"{nombre} no es una tupla"
        assert len(valor) == 3, f"{nombre} no tiene 3 componentes"
        assert all(isinstance(c, int) and 0 <= c <= 255 for c in valor), f"{nombre} fuera de rango"


def test_entidades_caben_en_un_tile():
    assert 0 < settings.PLAYER_SIZE <= settings.TILE_SIZE
    assert 0 < settings.TERMINAL_SIZE <= settings.TILE_SIZE


def test_valores_de_juego_son_positivos():
    assert settings.TIEMPO_LIMITE > 0
    assert settings.PLAYER_SPEED > 0
    assert settings.FPS > 0

import pytest

from src.puzzles import CATALOGO_PUZZLES

CAMPOS_REQUERIDOS = ("instruccion", "solucion", "pista")


def test_catalogo_no_esta_vacio():
    assert CATALOGO_PUZZLES


@pytest.mark.parametrize("task_id", sorted(CATALOGO_PUZZLES))
def test_puzzle_tiene_todos_los_campos(task_id):
    puzzle = CATALOGO_PUZZLES[task_id]

    for campo in CAMPOS_REQUERIDOS:
        assert puzzle.get(campo), f"el puzzle {task_id} no define '{campo}'"


@pytest.mark.parametrize("task_id", sorted(CATALOGO_PUZZLES))
def test_solucion_no_tiene_espacios_alrededor(task_id):
    # PuzzleManager compara input_text.strip() contra la solución: si la solución
    # trae espacios, el puzzle se vuelve irresoluble.
    solucion = CATALOGO_PUZZLES[task_id]["solucion"]

    assert solucion == solucion.strip()


def test_soluciones_son_unicas():
    soluciones = [puzzle["solucion"] for puzzle in CATALOGO_PUZZLES.values()]

    assert len(soluciones) == len(set(soluciones))

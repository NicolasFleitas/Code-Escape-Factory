import pytest

from src.puzzle_validators import VALIDATOR_TYPES, build_validator
from src.puzzles import CATALOGO_PUZZLES

CAMPOS_REQUERIDOS = ("instruccion", "solucion", "pista", "validator")


def test_catalogo_no_esta_vacio():
    assert CATALOGO_PUZZLES


@pytest.mark.parametrize("task_id", sorted(CATALOGO_PUZZLES))
def test_puzzle_tiene_todos_los_campos(task_id):
    puzzle = CATALOGO_PUZZLES[task_id]

    for campo in CAMPOS_REQUERIDOS:
        assert puzzle.get(campo), f"el puzzle {task_id} no define '{campo}'"


@pytest.mark.parametrize("task_id", sorted(CATALOGO_PUZZLES))
def test_solucion_no_tiene_espacios_alrededor(task_id):
    # The canonical solution is also what the puzzle shows and what the
    # validator parses: surrounding spaces would be dead data.
    solucion = CATALOGO_PUZZLES[task_id]["solucion"]

    assert solucion == solucion.strip()


@pytest.mark.parametrize("task_id", sorted(CATALOGO_PUZZLES))
def test_puzzle_declara_un_validador_conocido(task_id):
    assert CATALOGO_PUZZLES[task_id]["validator"] in VALIDATOR_TYPES


@pytest.mark.parametrize("task_id", sorted(CATALOGO_PUZZLES))
def test_la_solucion_pasa_su_propio_validador(task_id):
    puzzle = CATALOGO_PUZZLES[task_id]

    assert build_validator(puzzle).validate(puzzle["solucion"])



def test_soluciones_son_unicas():
    soluciones = [puzzle["solucion"] for puzzle in CATALOGO_PUZZLES.values()]

    assert len(soluciones) == len(set(soluciones))

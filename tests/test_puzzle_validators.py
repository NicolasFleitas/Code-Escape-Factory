"""Tests for the puzzle answer validators (one strategy per puzzle kind).

The validators are pure: they receive the answer text and return a bool, so
they run headless without pygame.
"""

import pytest

from src.puzzle_validators import (
    EXACT,
    PYTHON_ASSIGNMENT,
    VALIDATOR_TYPES,
    ExactTextValidator,
    PythonAssignmentValidator,
    build_validator,
)


def assignment(expected="energia = 100"):
    return PythonAssignmentValidator(expected)


@pytest.mark.parametrize(
    "answer",
    [
        "energia = 100",
        "energia=100",
        "  energia   =   100  ",
        "energia = 100  # valor inicial",
    ],
)
def test_python_assignment_accepts_equivalent_answers(answer):
    assert assignment().validate(answer)


@pytest.mark.parametrize(
    "answer",
    [
        "energia = 50",
        "energia2 = 100",
        "energia == 100",
        "energia =",
        "",
    ],
)
def test_python_assignment_rejects_wrong_answers(answer):
    assert not assignment().validate(answer)


def test_python_assignment_rejects_extra_statements():
    assert not assignment().validate("energia = 100\ncodigo = 1234")


def test_python_assignment_does_not_confuse_bool_and_int():
    puerta = PythonAssignmentValidator("puerta = True")

    assert puerta.validate("puerta = True")
    assert not puerta.validate("puerta = 1")
    assert not puerta.validate("puerta = 'True'")


def test_python_assignment_rejects_computed_values():
    # The puzzle asks for a literal, not an expression that happens to match.
    assert not assignment().validate("energia = 50 + 50")


def test_python_assignment_ignores_quote_style():
    ventilacion = PythonAssignmentValidator("ventilacion = 'ON'")

    assert ventilacion.validate('ventilacion = "ON"')
    assert not ventilacion.validate("ventilacion = ON")


def test_exact_validator_ignores_surrounding_whitespace():
    validator = ExactTextValidator("ALARMA")

    assert validator.validate("  ALARMA ")
    assert not validator.validate("alarma")


def test_build_validator_uses_the_declared_type():
    spec = {"solucion": "energia = 100", "validator": PYTHON_ASSIGNMENT}

    assert isinstance(build_validator(spec), PythonAssignmentValidator)


def test_build_validator_defaults_to_exact_text():
    assert isinstance(build_validator({"solucion": "ALARMA"}), ExactTextValidator)


def test_build_validator_rejects_unknown_types():
    with pytest.raises(ValueError, match="unknown"):
        build_validator({"solucion": "x = 1", "validator": "nope"})


def test_every_declared_type_is_registered():
    assert set(VALIDATOR_TYPES) == {EXACT, PYTHON_ASSIGNMENT}

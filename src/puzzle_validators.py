"""Answer validators for the programming puzzles.

Each puzzle declares which validator checks its answer, so the catalog can grow
with new kinds of exercises without touching PuzzleManager. Validators are pure
functions of the answer text: no pygame, no session state.
"""

import ast

EXACT = "exact"
PYTHON_ASSIGNMENT = "python_assignment"


class PuzzleValidator:
    """Interface every answer validator implements."""

    def validate(self, answer):
        raise NotImplementedError


class ExactTextValidator(PuzzleValidator):
    """Accept the canonical text, ignoring surrounding whitespace."""

    def __init__(self, expected):
        self.expected = expected.strip()

    def validate(self, answer):
        return answer.strip() == self.expected


class PythonAssignmentValidator(PuzzleValidator):
    """Accept one assignment whose variable and literal value match.

    Whitespace, comments and quote style are irrelevant: ``energia=100`` and
    ``energia = 100`` are the same answer. Anything that is not a single
    ``name = literal`` statement is rejected, and the literal types must match,
    so ``puerta = 1`` does not pass a ``puerta = True`` puzzle.
    """

    def __init__(self, expected):
        self.variable, self.value = _parse_assignment(expected)

    def validate(self, answer):
        try:
            variable, value = _parse_assignment(answer)
        except ValueError:
            return False

        return (
            variable == self.variable
            and type(value) is type(self.value)
            and value == self.value
        )


def _parse_assignment(source):
    """Return ``(variable, literal)`` for one ``name = literal`` statement."""
    try:
        module = ast.parse(source.strip(), mode="exec")
    except SyntaxError as error:
        raise ValueError(f"not valid Python: {source!r}") from error

    if len(module.body) != 1:
        raise ValueError(f"expected a single statement: {source!r}")

    statement = module.body[0]
    if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
        raise ValueError(f"expected one assignment: {source!r}")

    target = statement.targets[0]
    if not isinstance(target, ast.Name):
        raise ValueError(f"expected a variable name: {source!r}")

    try:
        value = ast.literal_eval(statement.value)
    except ValueError as error:
        raise ValueError(f"expected a literal value: {source!r}") from error

    return target.id, value


VALIDATOR_TYPES = {
    EXACT: ExactTextValidator,
    PYTHON_ASSIGNMENT: PythonAssignmentValidator,
}


def build_validator(puzzle):
    """Build the validator a puzzle declares; exact text is the fallback."""
    kind = puzzle.get("validator", EXACT)
    try:
        factory = VALIDATOR_TYPES[kind]
    except KeyError:
        raise ValueError(f"unknown puzzle validator: {kind!r}") from None

    return factory(puzzle["solucion"])

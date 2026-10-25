"""Catalog of programming puzzles.

Each puzzle declares the validator that checks its answer; ``solucion`` is the
canonical answer the validator parses (and the one the puzzle expects).
"""

CATALOGO_PUZZLES = {
    1: {
        "instruccion": "# BUG: La puerta esta cerrada (False). Corrigelo:",
        "solucion": "puerta = True",
        "pista": "PISTA: En Python, los booleanos empiezan con Mayúscula (True/False).",
        "validator": "python_assignment",
    },
    2: {
        "instruccion": "# ERROR: El sistema requiere energia. Declara energia = 100:",
        "solucion": "energia = 100",
        "pista": "PISTA: No dejes espacios en el nombre de la variable y usa un solo '='.",
        "validator": "python_assignment",
    },
    3: {
        "instruccion": "# SEGURIDAD: Define el código de acceso como 1234 (número):",
        "solucion": "codigo = 1234",
        "pista": "PISTA: Los números se escriben sin comillas. Ejemplo: valor = 55.",
        "validator": "python_assignment",
    },
    4: {
        "instruccion": "# SISTEMA: Activa los ventiladores configurando ventilacion = 'ON':",
        "solucion": "ventilacion = 'ON'",
        "pista": "PISTA: El texto (string) debe ir entre comillas simples o dobles: 'TEXTO'.",
        "validator": "python_assignment",
    },
}

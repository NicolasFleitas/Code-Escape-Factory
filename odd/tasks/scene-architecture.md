# Feature: scene-architecture — refactor de arquitectura de Code Escape: Factory Reset

Objective: ejecutar el roadmap de refactor persistido en Engram (`architecture/game-structure`, obs #615/#622) para que el juego pueda crecer (movimientos, efectos, puzzles) sin que `engine.py` sea un god object.
Branch: `refactor/scene-architecture`, cada paso del roadmap se entrega como PR con squash merge a `main`.
Delivery strategy: `auto-chain` (preferencia persistida del usuario: desarrollador único, auto-merge + branch protection configurados, sin aprobaciones manuales), chain strategy `stacked-to-main`, un paso del roadmap por PR. Test runner: `pytest` + `ruff check .`, headless only.

## Specs

S1 — Arquitectura de escenas (paso 1 del roadmap, verbatim de la memoria #615): "GameState enum, one Scene per state (Menu, CharacterSelect, Playing, Programming, Paused, GameOver) with handle_event/update(dt)/draw; Game becomes loop + scene router." Aceptación: `engine.py` sin lógica por estado; todo estado rutear a una escena; comportamiento observable conservado (menu, selección de personaje, explorar/programar, pausa, ganar/perder); tests unitarios fijan las transiciones; `ruff check .` y `pytest` en verde; se cumplen las reglas de CONTRIBUTING §6.

S2 — Delta time + adaptador de input (paso 2): "update(dt) con delta time e input como adaptador (Player.update(dt, direccion), sin pygame.key adentro)."

S3 — Mapas como datos (paso 3): "Mapas a archivo de datos + loader/renderer separados; resolver el 768 vs 720."

S4 — Puzzles por strategy (paso 4): "Puzzles por strategy/validator en vez de igualdad de strings."

S5 — Módulo único de assets (paso 5): "Modulo unico de assets con pathlib desde __file__."

S6 — Pendientes menores (del resumen de sesión anterior, verbatim): "bump de actions/checkout@v4 y actions/setup-python@v5 (Node 20 deprecado); eliminar codigo muerto (Player.set_custom_sprite, MapManager.draw_debug, AudioManager.handle_alarms, src/generate_assets.py)."

## Tasks

| ID | Specs | Route | Status | Evidence |
| --- | --- | --- | --- | --- |
| T1 | S1 | inline | done | RED→GREEN pytest 38 passed; ruff clean; smoke headless 10/10; PR #26 squash → main 5cdd087 |
| T2 | S2 | inline | pending | — |
| T3 | S3 | inline | pending | — |
| T4 | S4 | inline | pending | — |
| T5 | S5 | inline | pending | — |
| T6 | S6 | inline | pending | — |

Route notes: ningún Writer trigger aplica (cada tarea es una unidad cohesiva única, sin superficies paralelas); el padre trabaja inline siguiendo este documento.

## Log

L1 (2026-10-23, verbatim): "Quiero continuar con el refactor de arquitectura que hay pendiente. Esta anotado en engram"

L2: Contexto recuperado de Engram: roadmap en `architecture/game-structure` (obs #615), convenciones en `project/conventions` (obs #617), resumen de sesión en obs #622. La sesión anterior cerró el flujo Git (PR #24 y #25 mergeados; main en 2d9cd26; trunk-based configurado). Próximo paso registrado: "Arrancar el refactor en una rama refactor/scene-architecture: 1. GameState enum + una Scene por estado (Menu, CharacterSelect, Playing, Programming, Paused, GameOver); Game queda como loop + router."

L3: Delivery strategy registrada desde la preferencia persistida del usuario (sin PRs manuales; auto-merge y required check "ruff + pytest" activos). Pronóstico de T1 ~1000 líneas autoradas, supera el presupuesto de 400: es una unidad cohesiva única (partir la extracción de la máquina de estados dejaría un router medio viejo/medio nuevo en main), se acepta `size:exception` por trunk-based con desarrollador único y CI gating; T2-T6 continúan como PRs encadenados.

L4 (evidencia T1): RED observado: `ModuleNotFoundError: No module named 'src.game_state'` al correr los 25 tests nuevos antes de implementar. GREEN: implementados `src/game_state.py` (GameState enum), `src/scenes/` (base + Menu/CharacterSelect/Playing/Programming/Paused/GameOver), `engine.py` reescrito como loop + router (413→~160 líneas), `ui_manager.draw_end_screen` compara contra `GameState` en vez de magic strings, `sys.exit()` reemplazado por flag `running` (salida limpia del loop, testeable headless). Verificado: `pytest` 38 passed (13 previos + 25 nuevos, todos headless con Rect/Event sintéticos y mixer monkeypatcheado), `ruff check .` limpio, smoke con drivers dummy 10/10 (transiciones reales de todas las escenas, dibujado de las 7 escenas, run() exits tras QUIT). Risk: none (refactor preservando comportamiento, cubierto por tests de transiciones; sin ítems de alto riesgo 1-6).

L5: Entrega de T1: PR #26 creado con CI verde ("ruff + pytest" pass en 13s) y squash-mergeado a main como 5cdd087 (rama refactor/scene-architecture borrada). Assessment RDD del commit: risk medium (executable_change en engine.py), review_due false (under_budget), sin review nativo requerido; verificación de la unidad: suite 38 passed + smoke 10/10. Boundary de review avanza a 5cdd087 para los próximos commits.



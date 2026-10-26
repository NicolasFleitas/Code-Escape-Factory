# Feature: scene-architecture — refactor de arquitectura de Code Escape: Factory Reset

Objective: ejecutar el roadmap de refactor persistido en Engram (`architecture/game-structure`, obs #615/#622) para que el juego pueda crecer (movimientos, efectos, puzzles) sin que `engine.py` sea un god object.
Branch: una rama corta por paso (`refactor/scene-architecture` para T1; `refactor/player-delta-time`, `refactor/map-data`, `refactor/puzzle-validators`, `refactor/asset-paths` y `chore/pending-cleanups` para T2–T6), con PR y squash merge a `main`.
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
| T1 | S1 | inline | done | RED→GREEN pytest 38 passed; ruff clean; smoke headless 10/10; PR #26 squash → main 6dcbdc3 |
| T2 | S2 | inline | done | RED→GREEN pytest 62 passed; ruff clean; smoke headless con Game real (150 px en 0,5 s = 300 px/s); diferencial vs 66cdfb5: bloqueo por ejes idéntico, diagonal ahora normalizada (cambio intencional); PR #28 squash → main ef37d0c |
| T3 | S3 | inline | done | RED→GREEN pytest 83 passed; ruff clean; render pixel a pixel idéntico vs caa446c sobre 1280x768; smoke headless 7 escenas + puerta; PR #29 squash → main 789bde6 |
| T4 | S4 | inline | done | RED→GREEN pytest 112 passed; ruff clean; diferencial vs 211ecdf (112 respuestas, 0 regresiones, 6 aceptadas nuevas intencionales); smoke headless 4/4; review nativo aprobado (lineage review-4db4e047002d9690); PR #30 squash → main a3ee6a3 |
| T5 | S5 | inline | done | RED→GREEN pytest 121 passed; ruff clean; diferencial vs e532044: idéntico desde la raíz del repo, desde cwd ajeno el base perdía fondo de menú y audio; smoke con Game real desde cwd ajeno 7/7 escenas + audio; PR #31 squash → main 6a91f84 |
| T6 | S6 | inline | done | RED no aplicable (solo eliminación); grep de referencias = 0; pytest 121 passed; ruff clean; smoke headless desde cwd ajeno 7/7 escenas + audio; PR #32 squash → main 09ef9d3 |

Route notes: ningún Writer trigger aplica (cada tarea es una unidad cohesiva única, sin superficies paralelas); el padre trabaja inline siguiendo este documento.

## Log

L1 (2026-10-23): pedido del usuario: continuar con el refactor de arquitectura pendiente, registrado en Engram (roadmap architecture/game-structure).

L2: Contexto recuperado de Engram: roadmap en `architecture/game-structure` (obs #615), convenciones en `project/conventions` (obs #617), resumen de sesión en obs #622. La sesión anterior cerró el flujo Git (PR #24 y #25 mergeados; main en 2d9cd26; trunk-based configurado). Próximo paso registrado: "Arrancar el refactor en una rama refactor/scene-architecture: 1. GameState enum + una Scene por estado (Menu, CharacterSelect, Playing, Programming, Paused, GameOver); Game queda como loop + router."

L3: Delivery strategy registrada desde la preferencia persistida del usuario (sin PRs manuales; auto-merge y required check "ruff + pytest" activos). Pronóstico de T1 ~1000 líneas autoradas, supera el presupuesto de 400: es una unidad cohesiva única (partir la extracción de la máquina de estados dejaría un router medio viejo/medio nuevo en main), se acepta `size:exception` por trunk-based con desarrollador único y CI gating; T2-T6 continúan como PRs encadenados.

L4 (evidencia T1): RED observado: `ModuleNotFoundError: No module named 'src.game_state'` al correr los 25 tests nuevos antes de implementar. GREEN: implementados `src/game_state.py` (GameState enum), `src/scenes/` (base + Menu/CharacterSelect/Playing/Programming/Paused/GameOver), `engine.py` reescrito como loop + router (413→~160 líneas), `ui_manager.draw_end_screen` compara contra `GameState` en vez de magic strings, `sys.exit()` reemplazado por flag `running` (salida limpia del loop, testeable headless). Verificado: `pytest` 38 passed (13 previos + 25 nuevos, todos headless con Rect/Event sintéticos y mixer monkeypatcheado), `ruff check .` limpio, smoke con drivers dummy 10/10 (transiciones reales de todas las escenas, dibujado de las 7 escenas, run() exits tras QUIT). Risk: none (refactor preservando comportamiento, cubierto por tests de transiciones; sin ítems de alto riesgo 1-6).

L5: Entrega de T1: PR #26 creado con CI verde ("ruff + pytest" pass en 13s) y squash-mergeado a main como 6dcbdc3 (rama refactor/scene-architecture borrada). Assessment RDD del commit: risk medium (executable_change en engine.py), review_due false (under_budget), sin review nativo requerido; verificación de la unidad: suite 38 passed + smoke 10/10. Boundary de review avanza a 6dcbdc3 para los próximos commits.

L6 (2026-10-24): decisión del usuario: trackear uv.lock en el repositorio. Resuelto vía chore PR #27. El archivo es un lockfile mínimo de uv (solo requires-python >=3.13, sin paquetes: las dependencias viven en requirements.txt), sin impacto en código ni CI.

L7 (evidencia T2, rama `refactor/player-delta-time`):

- RED observado: `ModuleNotFoundError: No module named 'src.input_adapter'`, `ImportError: cannot import name 'clamp_delta_time'` y 13 fallos en `tests/test_player.py` (TypeError por la firma vieja `update(walls)`; un caso con `pygame.error`), más 2 fallos en `tests/test_scenes.py` (la escena no pasaba dt ni dirección). Un test extra de velocidad diagonal a 60 FPS falló con 339 px recorridos contra 300 esperados, lo que expuso un truncamiento de la posición flotante.
- Diseño: `src/input_adapter.py` es el único módulo que lee `pygame.key`; `read_movement_direction(keys)` es una función pura (ejes en -1/0/1, teclas opuestas se cancelan, flechas y WASD equivalen) e `InputAdapter` se inyecta en `Game` (`game.input`), igual que el resto de las dependencias. `PlayingScene.update(dt)` lee la dirección una vez por frame y llama `player.update(dt, direccion, walls)`.
- `Player.update(dt, direction=(0, 0), walls=())`: la velocidad pasa a píxeles por segundo (`PLAYER_SPEED = 300.0`, equivale a los 5 px/frame previos a 60 FPS). La posición real se guarda en un `Vector2` flotante y el `pygame.Rect` la refleja redondeada, así los pasos fraccionarios no se pierden. Los pasos se subdividen en tramos de `PLAYER_SIZE / 2` para que un frame largo no atraviese una pared. La dirección diagonal se normaliza y el eje horizontal conserva la prioridad de orientación. `block_left_of(blocker)` reemplaza la asignación directa de `rect.right` en la escena, manteniendo sincronizada la posición flotante.
- `clamp_delta_time(dt)` en `engine.py` limita el delta de cada frame a `MAX_DELTA_TIME = 0.05` s para que un stall (arrastre de ventana, breakpoint) no teletransporte al jugador.
- GREEN: `pytest` 62 passed (38 previos + 24 nuevos), `ruff check .` limpio. Smoke headless con el `Game` real y un input con guion: 150 px en 0,5 s hacia la derecha, dirección `derecha`, sin movimiento con dirección neutra; `draw()` sin excepciones.
- Diferencial contra 66cdfb5 (copia en directorio temporal, sin tocar el worktree): movimiento y bloqueo horizontal/vertical idénticos (160/160/64 px); la diagonal en espacio abierto pasa de 5 px por eje por frame (353 px/s) a 300 px/s normalizados. Es el único cambio observable y es intencional: la diagonal ya no es más rápida que la recta.
- Riesgo: ninguno de los ítems 1-6 (refactor de movimiento con tests nuevos; sin datos persistidos, seguridad, contratos públicos, concurrencia ni delivery).

L8 (entrega T2): PR #28 con CI verde ("ruff + pytest" pass en 12 s) squash-mergeado a main como ef37d0c; rama `refactor/player-delta-time` borrada. Assessment RDD del commit: risk medium (`executable_change` en `engine.py`), review_due false (`under_budget`), sin review nativo requerido. El boundary de review sigue en 66cdfb5 porque los commits under budget quedan pendientes dentro del slice. Próximo paso: T3 (mapas como datos).

L9 (evidencia T3, rama `refactor/map-data`):

- RED observado: `ModuleNotFoundError: No module named 'src.map_loader'` al correr los 21 tests nuevos antes de implementar.
- Diseño: `src/assets/maps/factory.json` declara dos capas (`floor` y `objects`) más una `legend` por símbolo (image, solid, terminal, door, spawn) y `door_open_image`. `src/map_loader.py` valida rectangularidad, símbolos declarados, roles únicos y deriva muros, terminales, puerta y spawn; `src/map_renderer.py` carga 21 tiles y dibuja primero el suelo y después los objetos. `MapManager` se elimina: también la inferencia de suelo por coordenadas (`_get_floor_type`) y la clave `"."` duplicada.
- Resolución 768 vs 720: el mapa es 20x12 tiles de 64 px = 1280x768. `SCREEN_HEIGHT` pasa a 768 para que el canvas coincida con el mundo completo (con `FULLSCREEN | SCALED` el letterboxing lo resuelve cada display); `test_map_fits_the_screen` fija el invariante que antes fallaba.
- GREEN: `pytest` 83 passed (62 previos + 21 nuevos), `ruff check .` limpio.
- Diferencial contra caa446c (copia temporal en `mktemp -d`, sin tocar el worktree): render pixel a pixel idéntico sobre 1280x768; muros (110), terminales (4), puerta (1216, 320) y spawn (576, 320) idénticos al MapManager viejo.
- Smoke headless con el `Game` real y drivers dummy: las 7 escenas dibujan, 150 px en 0,5 s, la puerta cerrada bloquea y la puerta abierta lleva a WON.
- Riesgo: ninguno de los ítems 1-6 (refactor interno con datos nuevos, tests y validación; sin datos persistidos, seguridad, contratos públicos, concurrencia ni delivery).

L10 (entrega T3): PR #29 con CI verde ("ruff + pytest" pass en 11 s) squash-mergeado a main como 789bde6; rama `refactor/map-data` borrada. Assessment RDD del slice 66cdfb5..789bde6: risk medium (`configuration_change` en `src/assets/maps/factory.json`), review_due false (`under_budget`), sin review nativo requerido; el boundary sigue en 66cdfb5. Próximo paso: T4 (puzzles por strategy/validator).

L11 (evidencia T4, rama `refactor/puzzle-validators`):

- RED observado: `ModuleNotFoundError: No module named 'src.puzzle_validators'` al correr los 29 tests nuevos antes de implementar.
- Diseño: `src/puzzle_validators.py` define la interfaz `PuzzleValidator` y dos estrategias: `ExactTextValidator` (texto canónico sin espacios alrededor, fallback del catálogo) y `PythonAssignmentValidator` (parsea con `ast` una única sentencia `nombre = literal` y compara nombre, valor y tipo; tolera espacios, comentarios y comillas simples/dobles, y rechaza expresiones, sentencias extra y confusión bool/int). `build_validator(puzzle)` arma la estrategia que declara el catálogo y falla ante un tipo desconocido.
- `src/puzzles.py`: cada puzzle declara `validator: "python_assignment"`; `solucion` sigue siendo la respuesta canónica que el validador parsea (sin duplicar la expectativa).
- `src/puzzle_manager.py`: `set_puzzle` construye el validador y `handle_event` delega el veredicto (`self.validator.validate(self.input_text)`); sin validador cargado no se puede resolver (antes, RETURN sin puzzle cargado resolvía por comparación con string vacío).
- Alcance: el split `PuzzleSession`/`PuzzleView` que menciona el paso 4 del roadmap no está en el texto citado de S4, así que queda fuera de esta tarea.
- GREEN: `pytest` 112 passed (83 previos + 29 nuevos), `ruff check .` limpio.
- Diferencial contra 211ecdf (catálogo base extraído en copia temporal fuera del worktree, sin tocar el worktree) sobre 112 respuestas: ninguna respuesta antes aceptada se rechaza ahora; 6 pasan a aceptarse (`puerta=True`, espacios múltiples, `energia = 100  # ok`, `codigo=1234`, `ventilacion = "ON"`), cambio intencional de la estrategia. Valores incorrectos, variables equivocadas, expresiones y sentencias extra siguen rechazados.
- Smoke headless con el `PuzzleManager` real (SDL dummy): los 4 puzzles se resuelven, la variante sin espacios también, y `draw()` no falla.
- Riesgo: ninguno de los ítems 1-6 (refactor interno de validación con tests; sin datos persistidos, seguridad, contratos públicos, concurrencia ni delivery).

L12 (entrega T4): PR #30 con CI verde ("ruff + pytest" pass en 11 s) squash-mergeado a main como a3ee6a3; rama `refactor/puzzle-validators` borrada. Assessment RDD del slice 66cdfb5..a3ee6a3: risk high (`process_boundary` en `src/puzzle_validators.py`), review_due true; consentimiento del usuario otorgado y review nativo con lentes readability + reliability aprobado (lineage review-4db4e047002d9690, 2 revisores, autoridad quemada). Sin blockers: 10 hallazgos informativos/advisories, con tres follow-ups accionables fuera del alcance de T4: el renderer identifica la puerta por el símbolo literal `"D"` en vez del rol del loader (`src/map_renderer.py:73`), ramas de error del loader sin test, y `Player.block_left_of` sin test contra el `Player` real. El boundary de review avanza a a3ee6a3. Próximo paso: T5 (módulo único de assets).

L13 (evidencia T5, rama `refactor/asset-paths`):

- RED observado: `ImportError: cannot import name 'asset_paths' from 'src' (unknown location)` al correr los 9 tests nuevos antes de implementar.
- Diseño: `src/asset_paths.py` es la única fuente de rutas: `ASSETS_DIR = Path(__file__).resolve().parent / "assets"`, los directorios `AUDIO_DIR`, `CHARACTERS_DIR`, `ITEMS_DIR`, `MAPS_DIR` y el helper `asset_path(*parts)`. Consumidores migrados: `audio_manager` (ambiente y efectos), `character_selector` (fondo y retratos), `ui_manager` (fondo del menú), `puzzle_manager` (sonido de error), `player` (sprites, sin duplicar la base con `os.path`), `map_loader` (toma `MAPS_DIR`) y `map_renderer` (toma `ITEMS_DIR`). `generate_assets.py` queda como está a propósito: es el generador one-off que T6 elimina, y ya resolvía desde `__file__`.
- GREEN: `pytest` 121 passed (112 previos + 9 nuevos), `ruff check .` limpio.
- Diferencial contra e532044 (copia en `/tmp/opencode`, sin tocar el worktree), en dos cwd distintos: desde la raíz del repo los digests son idénticos en los 21 tiles del mapa, los 4 sprites del jugador, el fondo del menú y los 3 sonidos + música. Desde un cwd ajeno el base fallaba en el fondo del menú (fallback gris) y en todo el audio (`None`); con el módulo nuevo carga todo igual que desde la raíz. El mapa y los sprites ya resolvían por `__file__` en el base, por eso no cambian: el arreglo observable es menú y audio, y es intencional.
- Smoke headless con el `Game` real desde `/tmp/opencode` (SDL dummy): audio cargado, música sonando, fondo de menú 1280x768 y las 7 escenas dibujan.
- Riesgo: ninguno de los ítems 1-6 (refactor interno de rutas con tests; sin datos persistidos, seguridad, contratos públicos, concurrencia ni delivery).

L14 (entrega T5): PR #31 con CI verde ("ruff + pytest" pass en 13 s) squash-mergeado a main como 6a91f84; rama `refactor/asset-paths` borrada. Assessment RDD del slice a3ee6a3..6a91f84: risk medium (`executable_change` en `src/asset_paths.py`), review_due false (`under_budget`), sin review nativo requerido; el boundary sigue en a3ee6a3 porque el commit queda pendiente dentro del slice. Próximo paso: T6 (pendientes menores).

L15 (evidencia T6, rama `chore/pending-cleanups`):

- CI: `.github/workflows/ci.yml` ya usa `actions/checkout@v4` y `actions/setup-python@v5` desde el PR #24 (commit a8b90b7); el bump pedido en S6 ya estaba aplicado y el workflow no cambia en esta tarea.
- Código muerto eliminado: `Player.set_custom_sprite` y el atributo `custom_sprite` (sin ninguna llamada en `src/` ni `tests/`); `AudioManager.handle_alarms` (las alarmas viven en `PlayingScene`/`Game` desde T1) junto con los seis flags de audio (`victoria_sound_played`, `victoria_sound_start_time`, `derrota_sound_played`, `derrota_sound_start_time`, `alarma_10s_played`, `alarma_5s_played`), que duplicaban el estado que ya es dueño `Game` (CONTRIBUTING §6) y solo se leían dentro del método borrado; `src/generate_assets.py` (generador one-off; los 43 assets están versionados).
- `MapManager.draw_debug` no existe en el árbol actual: `MapManager` se eliminó en T3 (L9), verificado por grep además de `MapManager`.
- Docs: se retira del README la sección "Generación de Assets" y la línea del árbol de archivos que mencionaba el script, en el mismo commit (CONTRIBUTING §5).
- Test-first: excepción documentada. No hay comportamiento nuevo que pueda fallar en RED: la tarea es eliminación de código sin llamadas y de un script sin tests. Verificación estructural: `grep -rn "set_custom_sprite|custom_sprite|handle_alarms|generate_assets|MapManager|draw_debug"` sobre `*.py`, `*.md`, `*.yml` y `*.toml` devuelve 0 coincidencias fuera del documento de feature.
- GREEN: `pytest` 121 passed (los mismos 121 de T5; ningún test dependía del código eliminado, incluido `test_playing_alarm_at_10s_plays_once`, que fija que la alarma sigue sonando desde la escena), `ruff check .` limpio.
- Smoke headless con el `Game` real desde `/tmp/opencode` (SDL dummy): audio cargado (victoria, derrota, alarma), las 7 escenas actualizan y dibujan, el jugador se mueve 150 px en 0,5 s, y `custom_sprite`/`handle_alarms`/`alarma_10s_played` ya no existen en `Player`/`AudioManager`.
- Riesgo: ninguno de los ítems 1-6 (eliminación de código muerto y docs; sin datos persistidos, seguridad, contratos públicos, concurrencia ni delivery).







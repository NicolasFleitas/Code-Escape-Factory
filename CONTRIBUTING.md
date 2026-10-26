# Guía de contribución

Este documento define cómo trabajamos en **Code Escape: Factory Reset**. Si algo acá no cierra, se discute en un issue antes de improvisarlo en un commit.

## 1. Flujo de ramas

Usamos **trunk-based development**: `main` es la única rama de larga vida.

- `main` siempre tiene que estar jugable. Es la fuente de verdad.
- **No existe `develop`.** Cualquier rama de integración intermedia agrega deriva y ambigüedad sin aportar nada en un proyecto de una sola persona.
- Cada cambio sale de `main` en una rama corta, con prefijo por tipo:

| Prefijo | Uso |
| --- | --- |
| `feat/<slug>` | Funcionalidad nueva |
| `fix/<slug>` | Corrección de un bug |
| `refactor/<slug>` | Cambio interno sin cambio de comportamiento |
| `docs/<slug>` | Documentación |
| `chore/<slug>` | Tooling, CI, dependencias |

Reglas del nombre: inglés, minúsculas, ASCII y con guiones (`feat/player-delta-time`). Nada de acentos, mayúsculas ni `14-feat-...` con el número del issue adelante. Si hay issue asociado, se referencia en el PR (`Closes #14`), no en el nombre de la rama.

Una rama = un cambio coherente. Si mientras trabajás aparece otra idea, va a otra rama. La rama se mergea en días, no en semanas.

## 2. Commits

**Conventional Commits, con la descripción en español.**

```
<tipo>(<alcance opcional>): <descripción en imperativo>
```

Ejemplos válidos:

```
feat(movimiento): agregar desplazamiento por delta time
fix(mapa): eliminar clave duplicada del tile de suelo
refactor(motor): extraer la máquina de estados a escenas
docs: documentar el flujo de contribución
chore(ci): correr ruff y pytest en cada pull request
```

- El `tipo` va en inglés (`feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`); la descripción va en español, en infinitivo y sin punto final.
- Un commit = un cambio con sentido propio. Si el mensaje necesita un "y", probablemente sean dos commits.
- **Prohibido** `Merge branch 'develop'` y cualquier merge commit generado por actualizar una rama. Se actualiza con `git rebase origin/main`.
- **Prohibido** agregar `Co-Authored-By` o cualquier atribución a herramientas de IA.

## 3. Pull requests

1. Actualizá la rama contra `main` con rebase.
2. Abrí el PR contra `main` completando: qué cambia, por qué, y cómo se verificó.
3. El PR tiene que pasar CI (ruff + pytest).
4. **Squash merge** siempre. Un PR = un commit en `main`.
5. Después del merge se borra la rama, local y remota:

```bash
git branch -D feat/mi-rama   # -D: el squash merge no deja los commits como ancestros de main
git push origin --delete feat/mi-rama
```

`-d` falla después de un squash merge porque los commits originales no quedan en el historial de `main`. Si el repositorio tiene activado *Automatically delete head branches*, el borrado remoto es automático y solo queda limpiar la rama local.

Nunca se commitea directo a `main`. La única excepción es una corrección trivial de una línea en documentación; la evidencia de tareas (`odd/tasks/*.md`) no entra en esa excepción.

## 4. Entorno local

Requisitos: Python 3.13 (fijado en `.python-version`) y [uv](https://github.com/astral-sh/uv).

```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
python main.py
```

`pygame==2.6.1` publica wheels hasta CPython 3.13. En 3.14 intenta compilar desde código fuente y falla sin las cabeceras de desarrollo de SDL2.

## 5. Verificación antes de pedir review

```bash
ruff check .
pytest
```

Los dos comandos tienen que pasar. Si agregás comportamiento, agregás su test. Si tocás un comando, una opción o un mensaje visible, actualizás la documentación en el mismo PR.

La evidencia del trabajo (`odd/tasks/<feature>.md`) se actualiza en el mismo PR que el cambio: la fila de la tarea registra el estado y las verificaciones, y el PR identifica la entrega. El SHA del squash se consulta en el historial (`git log`), porque no puede escribirse en el mismo commit que lo produce.

## 6. Reglas de arquitectura

Estas reglas existen para que el proyecto pueda crecer sin que `engine.py` se coma todo. Aplican a código nuevo y a refactors; no se exige reescribir lo viejo de golpe.

- **`Game` es solo el bucle y el router de escenas.** No es el lugar para lógica de juego, layout de botones ni carga de assets.
- **Cada estado del juego es una escena** con `handle_event`, `update(dt)` y `draw`.
- **El estado del juego tiene un único dueño.** No se duplican flags (por ejemplo, si un sonido ya se reprodujo) entre el motor y un manager.
- **Todo movimiento usa delta time** (`update(dt)`). Nada de píxeles fijos por frame.
- **Las entidades no leen el teclado.** `Player.update(dt, direccion)` recibe el input; no llama a `pygame.key.get_pressed()`.
- **Datos y render separados.** Mapas y puzzles son datos; los loaders y renderers van aparte.
- **Un solo módulo de rutas de assets**, resuelto desde `__file__` con `pathlib`. Prohibido `os.path.join("src", "assets", ...)` relativo al directorio de ejecución.
- **Nada de estado global mutable** importado entre módulos. Si dos módulos necesitan lo mismo, se inyecta.
- **La lógica tiene que poder correr headless.** Si un test necesita una ventana, la dependencia está mal ubicada.

## 7. Convenciones de código

- Python 3.13, sin dependencias nuevas sin justificarlo en el PR.
- Identificadores, comentarios y docstrings en inglés. La documentación de usuario (README, esta guía) en español.
- Nombres de archivos y módulos en `snake_case`.
- `ruff` es la única fuente de verdad de estilo. No se discute formato en los PRs.
- Un `print` de diagnóstico no llega a `main`; se usa `logging` o se elimina.

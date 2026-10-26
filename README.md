# 🏭 Code Escape: Factory Reset

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://www.pygame.org/)

**Code Escape: Factory Reset** es un juego de puzles y estrategia en 2D con estética pixel art. Encarnas a un operario de fábrica que debe restaurar los sistemas críticos antes de que se agote el tiempo para poder escapar de las instalaciones bloqueadas.

---

## 🚀 Características

- **Selección de Personaje:** Elige entre 3 operarios (Obrero, Jefe y Bombero), cada uno con su propio estilo visual.
- **Entornos Dinámicos:** Explora salas de oficina y áreas industriales con decoraciones detalladas como plantas, paneles de control, maquinaria y más.
- **Desafíos de Programación:** Interactúa con terminales para resolver puzles de asignación en Python (`nombre = valor`).
- **Sistema de Tiempo Real:** Tienes 60 segundos (`TIEMPO_LIMITE` en `settings.py`); el cronómetro se congela mientras el juego está en pausa.
- **Gráficos Pixel Art:** Estética top-down con assets versionados en `src/assets/`.
- **Interfaz Intuitiva:** Menús, selección de personaje y overlays de programación interactivos.

---

## 🕹️ Cómo Jugar

### Objetivo
Explora la fábrica, encuentra las **4 terminales**, resuelve sus puzles de código para abrir la puerta principal y escapa antes de que el cronómetro llegue a cero.

### Controles
- **Movimiento:** Teclas de dirección (↑, ↓, ←, →) o `WASD`.
- **Interactuar:** `E` cerca de una terminal.
- **Programar:** escribe la respuesta y confirma con `Enter`; `H` muestra u oculta la pista; `Esc` vuelve a la exploración.
- **Menús:** flechas y `Enter`, o mouse.
- **Pausa:** `Esc` durante la exploración; `Esc` de nuevo reanuda.
- **Pantalla final:** `←`/`→` y `Enter`, o mouse.
- **Salir:** opción `EXIT` del menú principal.

---

## 🛠️ Instalación y Uso

### Requisitos Previos
- Python 3.13 (fijado en `.python-version` y verificado en CI). `pygame==2.6.1` publica wheels hasta CPython 3.13; en 3.14 intenta compilar desde código fuente y falla sin las cabeceras de desarrollo de SDL2.
- Git.

### Instalación
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/NicolasFleitas/Code-Escape-Factory.git
   cd Code-Escape-Factory
   ```

2. **Crea y activa un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

   Con `uv` (respeta `.python-version`, que fija Python 3.13):
   ```bash
   uv venv --python 3.13
   uv pip install -r requirements.txt -r requirements-dev.txt
   ```

### Ejecución
Para iniciar el juego:
```bash
python main.py
```

### Verificación
Requiere las dependencias de desarrollo (`pip install -r requirements-dev.txt`).
```bash
ruff check .
pytest
```

---

## 📂 Estructura del Proyecto

```text
Code-Escape-Factory/
├── main.py                     # Punto de entrada del juego
├── pyproject.toml              # Configuración de pytest y ruff
├── requirements.txt            # Dependencias de ejecución
├── requirements-dev.txt        # Dependencias de desarrollo (pytest, ruff)
├── uv.lock                     # Lockfile mínimo de uv
├── CONTRIBUTING.md             # Flujo de ramas, commits y arquitectura
├── DOCUMENTACION_FLUJO.md      # Flujo de estados y reglas de negocio
├── src/
│   ├── assets/                 # Sprites, mapa JSON y audio versionados
│   ├── asset_paths.py          # Única fuente de rutas de assets
│   ├── engine.py               # Loop principal y router de escenas
│   ├── game_state.py           # Enum GameState
│   ├── scenes/                 # Una escena por estado
│   │   ├── base.py
│   │   ├── menu.py
│   │   ├── character_select.py
│   │   ├── playing.py
│   │   ├── programming.py
│   │   ├── paused.py
│   │   └── game_over.py
│   ├── map_loader.py           # Carga factory.json y deriva muros y entidades
│   ├── map_renderer.py         # Dibuja las capas del mapa
│   ├── player.py               # Entidad del jugador, movimiento y sprites
│   ├── input_adapter.py        # Adaptador de teclado
│   ├── terminal.py             # Entidad terminal
│   ├── puzzle_manager.py       # Estado y UI del puzzle activo
│   ├── puzzles.py              # Catálogo de desafíos de código
│   ├── puzzle_validators.py    # Estrategias de validación
│   ├── character_selector.py   # Pantalla de selección de operario
│   ├── ui_manager.py           # Menús, HUD y overlays
│   ├── audio_manager.py        # Música y efectos de sonido
│   └── settings.py             # Constantes globales
├── tests/                      # Suite headless (pytest)
├── odd/tasks/                  # Documentos de features
└── .github/workflows/ci.yml    # CI: ruff + pytest
```

---

## 📚 Documentación

- [`CONTRIBUTING.md`](CONTRIBUTING.md): flujo de ramas, commits, PRs y reglas de arquitectura.
- [`DOCUMENTACION_FLUJO.md`](DOCUMENTACION_FLUJO.md): máquina de estados, controles y reglas de negocio.

---

## 💻 Tecnologías Utilizadas

- **Lenguaje:** [Python 3.13](https://www.python.org/)
- **Biblioteca Gráfica:** [pygame 2.6.1](https://www.pygame.org/)
- **Lógica de Juego:** Programación orientada a objetos (POO), con una escena por estado.

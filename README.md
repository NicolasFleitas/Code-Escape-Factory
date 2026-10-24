# 🏭 Code Escape: Factory Reset

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)](https://www.pygame.org/)

**Code Escape: Factory Reset** es un emocionante juego de puzles y estrategia en 2D con estética pixel art. Encarnas a un operario de fábrica que debe restaurar los sistemas críticos antes de que se agote el tiempo para poder escapar de las instalaciones bloqueadas.

---

## 🚀 Características

- **Selección de Personaje:** Elige entre 3 operarios diferentes, cada uno con su propio estilo visual (Pepe, Pedro y Juan).
- **Entornos Dinámicos:** Explora salas de oficina y áreas industriales con decoraciones detalladas como plantas, servidores, maquinaria y más.
- **Desafíos de Programación:** Interactúa con terminales para resolver puzles basados en lógica y sintaxis de código (Python style).
- **Sistema de Tiempo Real:** Gestiona tu tiempo con cuidado; la energía de la fábrica es limitada.
- **Gráficos Pixel Art:** Estética top-down con assets generados dinámicamente.
- **Interfaz Intuitiva:** Menús, selección de personaje y overlays de programación interactivos.

---

## 🕹️ Cómo Jugar

### Objetivo
Explora la fábrica, encuentra las **4 terminales**, resuelve sus puzles de código para abrir la puerta principal y escapa antes de que el cronómetro llegue a cero.

### Controles
- **Movimiento:** Teclas de dirección (↑, ↓, ←, →) o `WASD`.
- **Interactuar:** Tecla `E` (cuando estés cerca de una terminal o puerta).
- **Navegar Menús:** Flechas y `Enter`.
- **Salir/Pausar:** Tecla `Esc`.

---

## 🛠️ Instalación y Uso

### Requisitos Previos
- Python 3.10 a 3.13. `pygame==2.6.1` no publica wheels para Python 3.14, por lo que en 3.14 intenta compilar desde código fuente y falla sin las cabeceras de desarrollo de SDL2.
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
   uv venv
   uv pip install -r requirements.txt
   ```

### Ejecución
Para iniciar el juego:
```bash
python main.py
```

### Generación de Assets
Si deseas regenerar los assets base del juego:
```bash
python src/generate_assets.py
```

---

## 📂 Estructura del Proyecto

```text
Code-Escape-Factory/
├── main.py                 # Punto de entrada del juego
├── requirements.txt        # Dependencias del proyecto
├── src/
│   ├── assets/             # Recursos visuales y de audio
│   ├── engine.py           # Núcleo del juego y gestión de estados
│   ├── map_manager.py      # Lógica de renderizado de mapas y colisiones
│   ├── player.py           # Entidad del jugador y animaciones
│   ├── ui_manager.py       # Gestión de la interfaz de usuario
│   ├── puzzle_manager.py   # Lógica de los terminales y puzles
│   ├── puzzles.py          # Catálogo de desafíos de código
│   ├── character_selector.py # Pantalla de selección de operario
│   ├── audio_manager.py    # Gestión de música y efectos de sonido
│   ├── settings.py         # Configuraciones globales y constantes
│   └── generate_assets.py  # Script de creación dinámica de assets
└── README.md
```

---

## 💻 Tecnologías Utilizadas

- **Lenguaje:** [Python 3.13](https://www.python.org/)
- **Biblioteca Gráfica:** [Pygame CE](https://pyga.me/)
- **Lógica de Juego:** Programación orientada a objetos (POO).

---

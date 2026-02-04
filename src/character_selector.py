import pygame
import os
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO_SELECCION = (255, 0, 0)

class CharacterSelector:
    def __init__(self, screen):
        self.screen = screen
        
        # Variables de estado (preservando nombres exactos)
        self.indice_seleccionado = 0
        self.personaje_elegido = None
        self.imagen_elegida = None
        self.en_menu = True
        
        # Fuentes
        self.fuente = pygame.font.SysFont("Arial", 30)
        self.fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
        
        # Cargar recursos
        self._cargar_recursos()
    
    def _cargar_imagen(self, ruta, ancho, alto, alpha=False):
        """Carga una imagen con manejo de errores"""
        try:
            img = pygame.image.load(ruta)
            if alpha:
                img = img.convert_alpha()
            else:
                img = img.convert()
            return pygame.transform.scale(img, (ancho, alto))
        except Exception as e:
            print(f"Error: No se pudo cargar {ruta} - {e}")
            # Si falla, crea un cuadro gris para que el juego no se cierre
            superficie_error = pygame.Surface((ancho, alto))
            superficie_error.fill((100, 100, 100))
            return superficie_error
    
    def _cargar_recursos(self):
        """Carga el fondo y los personajes"""
        # Fondo
        ruta_fondo = os.path.join("src", "assets", "fondo1.jpeg")
        self.imagen_fondo = self._cargar_imagen(ruta_fondo, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Personajes (preservando nombre exacto de variable)
        # Cargamos la imagen de frente de cada obrero
        nombres_archivos = [
            "obrero1-frente.png",
            "obrero2-frente.png",
            "obrero3-frente.png"
        ]
        
        self.lista_personajes_img = []
        for nombre in nombres_archivos:
            ruta = os.path.join("src", "assets", "personajes", nombre)
            self.lista_personajes_img.append(self._cargar_imagen(ruta, 150, 150, alpha=True))
        
        # Nombres de personajes
        self.personajes_nombres = ["Pepe (Obrero 1)", "Pedro (Obrero 2)", "Juan (Obrero 3)"]

        
        # Calcular áreas de interacción (Rects) para el mouse
        self.rects = []
        self._calcular_rects()

    def _calcular_rects(self):
        """Calcula las posiciones de los cuadros de personajes"""
        ancho_caja, alto_caja = 150, 150
        espaciado = 200 
        ancho_total_grupo = (len(self.personajes_nombres) - 1) * espaciado
        inicio_x = (SCREEN_WIDTH - ancho_total_grupo) // 2 

        self.rects = []
        for i in range(len(self.personajes_nombres)):
            x = inicio_x + (i * espaciado) - (ancho_caja // 2)
            y = SCREEN_HEIGHT // 2 - (alto_caja // 2)
            # El área interactiva incluye el borde (ancho_caja + 20)
            rect = pygame.Rect(x - 10, y - 10, ancho_caja + 20, alto_caja + 20)
            self.rects.append(rect)
    
    def dibujar_menu(self):
        """Dibuja la interfaz de selección de personajes"""
        # Dibujar Fondo
        if self.imagen_fondo:
            self.screen.blit(self.imagen_fondo, (0, 0))
        
        # Título con sombra
        titulo = self.fuente_titulo.render("ELIGE TU PERSONAJE", True, BLANCO)
        sombra = self.fuente_titulo.render("ELIGE TU PERSONAJE", True, NEGRO)
        self.screen.blit(sombra, (SCREEN_WIDTH // 2 - titulo.get_width() // 2 + 2, 52))
        self.screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 50))
        
        # Configuración de los cuadros
        ancho_caja, alto_caja = 150, 150
        
        for i, rect_personaje in enumerate(self.rects):
            # Coordenadas internas para imagen y texto (basadas en el rect calculado)
            x = rect_personaje.x + 10
            y = rect_personaje.y + 10
            
            if i == self.indice_seleccionado:
                # Resaltado para el seleccionado
                pygame.draw.rect(self.screen, ROJO_SELECCION, rect_personaje, 5)
                texto_color = ROJO_SELECCION
            else:
                # Sombra para los no seleccionados
                s = pygame.Surface((ancho_caja, alto_caja))
                s.set_alpha(150)
                s.fill(NEGRO)
                self.screen.blit(s, (x, y))
                texto_color = BLANCO

            # DIBUJAR LA IMAGEN DEL PERSONAJE
            self.screen.blit(self.lista_personajes_img[i], (x, y))
            
            # Nombre centrado
            nombre = self.fuente.render(self.personajes_nombres[i], True, texto_color)
            self.screen.blit(nombre, (x + ancho_caja // 2 - nombre.get_width() // 2, y + alto_caja + 20))
    
    def handle_event(self, event):
        """Maneja los eventos de selección"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.indice_seleccionado = (self.indice_seleccionado + 1) % len(self.personajes_nombres)
            elif event.key == pygame.K_LEFT:
                self.indice_seleccionado = (self.indice_seleccionado - 1) % len(self.personajes_nombres)
            elif event.key == pygame.K_RETURN:
                # Confirmar selección
                self.personaje_elegido = self.personajes_nombres[self.indice_seleccionado]
                self.imagen_elegida = self.lista_personajes_img[self.indice_seleccionado]
                self.en_menu = False
                return True  # Indica que se completó la selección
        
        elif event.type == pygame.MOUSEMOTION:
            # Hover: Actualizar selección si el mouse está sobre un personaje
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.indice_seleccionado = i
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click: Confirmar selección si se hace clic en un personaje
            if event.button == 1:  # Clic izquierdo
                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(event.pos):
                        self.indice_seleccionado = i
                        self.personaje_elegido = self.personajes_nombres[self.indice_seleccionado]
                        self.imagen_elegida = self.lista_personajes_img[self.indice_seleccionado]
                        self.en_menu = False
                        return True

        return False  # Aún en proceso de selección
    
    def get_selected_character(self):
        """Retorna el personaje y la imagen seleccionados"""
        return self.personaje_elegido, self.imagen_elegida

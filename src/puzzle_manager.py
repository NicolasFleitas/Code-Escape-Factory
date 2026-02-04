import pygame
import os
from src.settings import COLOR_SUCCESS, COLOR_TEXTO, COLOR_ERROR
from src.puzzles import CATALOGO_PUZZLES  # Importamos el catálogo


class PuzzleManager:
    def __init__(self):
        self.input_text = ""
        self.target_code = ""
        self.instruction = ""
        self.pista = ""
        self.manual_pista = False # Nueva bandera para mostrar pista con H
        self.is_solved = False
        self.show_error = False
        self.error_timer = 0
        self.font = pygame.font.SysFont("monospace", 24)
        
        # Cargar sonido de error
        try:
            ruta_error = os.path.join("src", "assets", "audio", "error.mp3")
            self.error_sound = pygame.mixer.Sound(ruta_error)
            self.error_sound.set_volume(0.5)  # Volumen al 50%
        except Exception as e:
            print(f"No se pudo cargar el sonido de error: {e}")
            self.error_sound = None

    def set_puzzle(self, task_id):
        """Carga los datos de un puzzle específico del catálogo"""
        puzzle_data = CATALOGO_PUZZLES.get(task_id)
        if puzzle_data:
            self.instruction = puzzle_data["instruccion"]
            self.pista = puzzle_data.get("pista", "")
            self.target_code = puzzle_data["solucion"]
            self.input_text = ""
            self.manual_pista = False
            self.is_solved = False
            self.show_error = False
            self.error_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.input_text.strip() == self.target_code:
                    self.is_solved = True
                    self.show_error = False
                    return "SOLVED"
                else:
                    self.show_error = True
                    self.error_timer = pygame.time.get_ticks()
                    # Reproducir sonido de error
                    if self.error_sound:
                        self.error_sound.play()
            elif event.key == pygame.K_h: # Tecla H para ayuda
                self.manual_pista = not self.manual_pista
            else:
                # Si el usuario empieza a escribir de nuevo, quitamos el error
                self.show_error = False
                # Solo agregamos caracteres si no es la tecla H (para evitar escribir 'h' accidentalmente)
                if event.key != pygame.K_h and len(self.input_text) < 25:
                    self.input_text += event.unicode
        return None

    def draw(self, surface):
        # Manejar parpadeo de error (2 segundos)
        if self.show_error and pygame.time.get_ticks() - self.error_timer > 2000:
            self.show_error = False

        # Dibujar instrucción cargada dinámicamente
        instr = self.font.render(self.instruction, True, (150, 150, 150))
        surface.blit(instr, (100, 200))

        # Dibujar lo que el usuario escribe
        color = COLOR_TEXTO
        if self.is_solved:
            color = COLOR_SUCCESS
        elif self.show_error:
            # Efecto de parpadeo simple
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                color = COLOR_ERROR
        
        code_surface = self.font.render(f">>> {self.input_text}", True, color)
        surface.blit(code_surface, (100, 250))

        if self.is_solved:
            msg = self.font.render(
                "SISTEMA DESBLOQUEADO. Presiona ESC.", True, COLOR_SUCCESS
            )
            surface.blit(msg, (100, 350))
        elif self.show_error:
            err_msg = self.font.render(
                "ERROR DE SINTAXIS. Comando no reconocido.", True, COLOR_ERROR
            )
            surface.blit(err_msg, (100, 350))
            
            # Dibujar la pista debajo del error
            pista_surf = self.font.render(self.pista, True, (200, 200, 100))
            surface.blit(pista_surf, (100, 400))
        
        # Mostrar pista si se presiona H (aunque no haya error)
        if self.manual_pista and not self.is_solved:
            pista_surf = self.font.render(f"AYUDA: {self.pista}", True, (200, 200, 100))
            surface.blit(pista_surf, (100, 450))
        
        # Leyenda de ayuda
        if not self.is_solved:
            hint_msg = self.font.render("Presiona [H] para ver/ocultar pista", True, (80, 80, 80))
            surface.blit(hint_msg, (100, 550))

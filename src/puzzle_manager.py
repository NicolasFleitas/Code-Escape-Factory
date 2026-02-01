import pygame
from src.settings import COLOR_SUCCESS, COLOR_TEXTO
from src.puzzles import CATALOGO_PUZZLES  # Importamos el catálogo


class PuzzleManager:
    def __init__(self):
        self.input_text = ""
        self.target_code = ""
        self.instruction = ""
        self.is_solved = False
        self.font = pygame.font.SysFont("monospace", 24)

    def set_puzzle(self, task_id):
        """Carga los datos de un puzzle específico del catálogo"""
        puzzle_data = CATALOGO_PUZZLES.get(task_id)
        if puzzle_data:
            self.instruction = puzzle_data["instruccion"]
            self.target_code = puzzle_data["solucion"]
            self.input_text = ""
            self.is_solved = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.input_text.strip() == self.target_code:
                    self.is_solved = True
                    return "SOLVED"
            else:
                # Limitar longitud para que no se salga de la pantalla
                if len(self.input_text) < 25:
                    self.input_text += event.unicode
        return None

    def draw(self, surface):
        # Dibujar instrucción cargada dinámicamente
        instr = self.font.render(self.instruction, True, (150, 150, 150))
        surface.blit(instr, (100, 200))

        # Dibujar lo que el usuario escribe
        color = COLOR_SUCCESS if self.is_solved else COLOR_TEXTO
        code_surface = self.font.render(f">>> {self.input_text}", True, color)
        surface.blit(code_surface, (100, 250))

        if self.is_solved:
            msg = self.font.render(
                "SISTEMA DESBLOQUEADO. Presiona ESC.", True, COLOR_SUCCESS
            )
            surface.blit(msg, (100, 350))

import pygame
from src.settings import COLOR_SUCCESS, COLOR_TEXTO


class PuzzleManager:
    def __init__(self):
        self.input_text = ""
        self.target_code = "puerta = True"
        self.is_solved = False
        self.font = pygame.font.SysFont("monospace", 24)

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
        # Dibujar instrucciones y código
        instr = self.font.render(
            "# BUG: La puerta esta cerrada (False). Corrigelo:", True, (150, 150, 150)
        )
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

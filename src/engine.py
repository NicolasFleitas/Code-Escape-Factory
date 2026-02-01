import pygame
import sys
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    COLOR_FONDO,
    COLOR_DOOR,
    COLOR_DOOR_OPEN,
    COLOR_ERROR,
    COLOR_SUCCESS,
    COLOR_TIEMPO,
    TIEMPO_LIMITE,
)
from src.player import Player
from src.terminal import Terminal
from src.puzzle_manager import PuzzleManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Code Escape: Factory Reset")
        self.clock = pygame.time.Clock()

        # Fuentes
        self.font_ui = pygame.font.SysFont("monospace", 20)
        self.font_final = pygame.font.SysFont("monospace", 40, bold=True)

        # Instancias
        self.player = Player()
        self.pc_terminal = Terminal(600, 150, task_id=1)
        self.puzzle = PuzzleManager()

        # Propiedades de la Puerta
        self.door_rect = pygame.Rect(350, 0, 100, 30)
        self.puerta_abierta = False

        # Lógica de Tiempo
        self.inicio_ticks = pygame.time.get_ticks()

        # Estados: "EXPLORANDO", "PROGRAMANDO", "PERDIDO", "GANASTE"
        self.game_state = "EXPLORANDO"
        self.tiempo_restante = TIEMPO_LIMITE

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == "EXPLORANDO":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    # CARGAMOS EL PUZZLE SEGÚN EL ID DE LA TERMINAL
                    self.puzzle.set_puzzle(self.pc_terminal.task_id)
                    self.game_state = "PROGRAMANDO"

            elif self.game_state == "PROGRAMANDO":
                result = self.puzzle.handle_event(event)
                if result == "SOLVED":
                    self.puerta_abierta = True
                    # No regresamos inmediatamente para que el usuario vea el éxito

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state = "EXPLORANDO"

    def update(self):
        # --- Gestión de Tiempo ---
        if self.game_state not in ["PERDIDO", "GANASTE"]:
            segundos_transcurridos = (
                pygame.time.get_ticks() - self.inicio_ticks
            ) // 1000
            self.tiempo_restante = max(0, TIEMPO_LIMITE - segundos_transcurridos)

            if self.tiempo_restante <= 0:
                self.game_state = "PERDIDO"

        # --- Lógica de Movimiento y Victoria ---
        if self.game_state == "EXPLORANDO":
            self.player.update()

            # Si la puerta está cerrada, bloquea el paso
            if not self.puerta_abierta:
                if self.player.rect.colliderect(self.door_rect):
                    self.player.rect.top = self.door_rect.bottom
            else:
                # Si la puerta está ABIERTA y el jugador la toca -> ¡GANA!
                if self.player.rect.colliderect(self.door_rect):
                    self.game_state = "GANASTE"

    def draw(self):
        self.screen.fill(COLOR_FONDO)

        if self.game_state != "PERDIDO" and self.game_state != "GANASTE":
            # 1. Dibujar Puerta (Cambia de color según el estado)
            color_actual_puerta = COLOR_DOOR_OPEN if self.puerta_abierta else COLOR_DOOR
            pygame.draw.rect(self.screen, color_actual_puerta, self.door_rect)

            # 2. Dibujar Elementos
            self.pc_terminal.draw(self.screen, self.player.rect)
            self.player.draw(self.screen)

            # 3. Dibujar UI de Energía
            timer_text = self.font_ui.render(
                f"ENERGIA LINTERNA: {self.tiempo_restante}s", True, COLOR_TIEMPO
            )
            self.screen.blit(timer_text, (20, 20))

            # 4. Overlay de Terminal
            if self.game_state == "PROGRAMANDO":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(230)
                overlay.fill((5, 10, 5))
                self.screen.blit(overlay, (0, 0))
                self.puzzle.draw(self.screen)

        elif self.game_state == "PERDIDO":
            self.screen.fill((0, 0, 0))
            msg = self.font_final.render("LINTERNA APAGADA", True, COLOR_ERROR)
            msg_sub = self.font_ui.render(
                "Te has quedado atrapado en la oscuridad.", True, (100, 100, 100)
            )
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(
                msg_sub, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 30)
            )

        elif self.game_state == "GANASTE":
            self.screen.fill((20, 50, 20))  # Fondo verde oscuro
            msg = self.font_final.render("¡GANASTE!", True, COLOR_SUCCESS)
            msg_sub = self.font_ui.render(
                "Has escapado de la fabrica a tiempo.", True, (255, 255, 255)
            )
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(
                msg_sub, (SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 30)
            )

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()

import sys
from typing import Literal, Optional

import pygame
import pygame_gui
import sympy as sp

from tools import convert_latex, differentiate, parse_function, return_latex_surface


class Derivative:
    def __init__(self, WIDTH: int, HEIGHT: int, surface) -> None:

        self.WIDTH = WIDTH

        self.HEIGHT = HEIGHT

        self.surface = surface

        self.clock = pygame.time.Clock()

        self.x = sp.Symbol("x")

        self.running = True

        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))

        self.input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (((self.WIDTH - (self.WIDTH // 3.6)) // 2), 100),
                (self.WIDTH // 3.6, 50),
            ),
            manager=self.manager,
            placeholder_text="Enter function (e.g., x^2)",
        )

        self.order_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (((self.WIDTH - (self.WIDTH // 3.6)) // 2), 160),
                (self.WIDTH // 7.2 - 5, 50),
            ),
            manager=self.manager,
            placeholder_text="Order (Default: 1)",
        )

        self.calculate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (
                    ((self.WIDTH - (self.WIDTH // 3.6)) // 2)
                    + (self.WIDTH // 7.2)
                    + 10,
                    160,
                ),
                (self.WIDTH // 7.2 - 10, 50),
            ),
            text="Calculate",
            manager=self.manager,
        )

        self.derivative_expression = None

        self.error_message = None

        self.font = pygame.font.SysFont(None, 28)

    def calculate_derivative(self):

        self.error_message = None

        expression_raw = self.input_box.get_text().strip()

        order_raw = self.order_box.get_text().strip()

        if not expression_raw:
            self.error_message = "Error: Please enter an expression."

            return

        if order_raw == "":
            order = 1

        else:
            try:
                order = int(order_raw)

                if order < 1:
                    raise ValueError

            except ValueError:
                self.error_message = "Error: Order must be a positive integer."

                return

        try:
            parsed_expr = parse_function(expression_raw)

            self.derivative_expression = self.derivative(parsed_expr, order)

        except Exception:
            self.derivative_expression = None

            self.error_message = "Math Error: Invalid expression structure."

    def derivative(self, expression, order=1):

        return differentiate(expression, self.x, order)

    def run(self) -> Optional[Literal["menu"]]:

        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH = max(720, event.w)

                    self.HEIGHT = max(406, event.h)

                    self.surface = pygame.display.set_mode(
                        (self.WIDTH, self.HEIGHT), pygame.RESIZABLE
                    )

                    self.manager.set_window_resolution((self.WIDTH, self.HEIGHT))

                    self.input_box.set_dimensions((self.WIDTH // 3.6, 50))

                    self.input_box.set_position(
                        ((self.WIDTH - (self.WIDTH // 3.6)) // 2, 100)
                    )

                    self.order_box.set_dimensions((self.WIDTH // 7.2, 50))

                    self.order_box.set_position(
                        ((self.WIDTH - (self.WIDTH // 3.6)) // 2, 160)
                    )

                    self.calculate_button.set_dimensions((self.WIDTH // 7.2 - 10, 50))

                    self.calculate_button.set_position(
                        (
                            ((self.WIDTH - (self.WIDTH // 3.6)) // 2)
                            + (self.WIDTH // 7.2)
                            + 10,
                            160,
                        )
                    )

                self.manager.process_events(event)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.calculate_button:
                        self.calculate_derivative()

                        if self.derivative_expression is not None:
                            self.result_surf = return_latex_surface(
                                convert_latex(self.derivative_expression)
                            )

            self.surface.fill((255, 255, 255))

            self.manager.update(time_delta)

            self.manager.draw_ui(self.surface)

            if self.error_message:
                error_surf = self.font.render(self.error_message, True, (200, 50, 50))

                self.surface.blit(error_surf, (100, 300))

            elif self.derivative_expression is not None:
                self.surface.blit(self.result_surf, (100, 300))

            pygame.display.flip()

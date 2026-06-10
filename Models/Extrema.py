import sys

import pygame
import pygame_gui

from tools import convert_latex, find_extrema, return_latex_surface


class Extrema:
    def __init__(self, surface, width, height):
        self.surface = surface
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((width, height))
        self.extrema_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (((self.width - (self.width // 3.6)) // 2), 100),
                (self.width // 3.6, 50),
            ),
            manager=self.manager,
            placeholder_text="Expression",
        )
        self.extrema_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (((self.width - (self.width // 3.6)) // 2), 160),
                (self.width // 3.6, 50),
            ),
            text="Calculate",
            manager=self.manager,
        )
        self.running = True
        self.error_message = None
        self.extrema = None
        self.font = pygame.font.SysFont("Arial", 28)

    def max_min(self):
        self.error_message = None
        self.raw_string = self.extrema_input.get_text().strip()
        if not self.raw_string:
            self.error_message = "Error: Please enter an expression."
            return
        try:
            self.extrema = find_extrema(self.raw_string)
        except Exception:
            self.extrema = None
            self.error_message = "Error Parsing Expression"

    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.type == pygame.VIDEORESIZE:
                    self.width = max(720, event.w)
                    self.height = max(406, event.h)
                    self.surface = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE
                    )
                    self.manager.set_window_resolution((self.width, self.height))
                    self.extrema_button.set_position(
                        (((self.width - (self.width // 3.6)) // 2), 160)
                    )
                    self.extrema_button.set_dimensions((self.width // 3.6, 50))
                    self.extrema_input.set_position(
                        (((self.width - (self.width // 3.6)) // 2), 100)
                    )
                    self.extrema_input.set_dimensions((self.width // 3.6, 50))
                self.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.extrema_button:
                        self.max_min()
                        if self.extrema is not None:
                            result = return_latex_surface(convert_latex(self.extrema))
            self.surface.fill((255, 255, 255))
            self.manager.update(time_delta)
            self.manager.draw_ui(self.surface)
            if self.error_message:
                error_surf = self.font.render(self.error_message, True, (200, 50, 50))
                self.surface.blit(error_surf, (100, 230))
            elif self.extrema is not None:
                self.surface.blit(result, (100, 230))
            pygame.display.flip()

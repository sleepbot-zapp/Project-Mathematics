import pygame as pygame
import sys
import pygame_gui
import sympy as sp

from Tools.integrator import integrate
from Tools.parse_function import parse_function
from Tools.convert_latex import return_latex_surface, convert_latex

class Integral:

    def __init__(self, WIDTH, HEIGHT, surface):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.surface = surface
        self.x = sp.Symbol('x')
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        self.input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((((self.WIDTH -(self.WIDTH // 3.6))//2), 100), (self.WIDTH // 3.6, 50)), 
            manager=self.manager,
            placeholder_text="Enter function (e.g., x**2)"
        )
        self.calculate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((((self.WIDTH -(self.WIDTH // 3.6))//2), 160), (self.WIDTH//3.6, 50)),
            text="Calculate",
            manager=self.manager
        )
        self.running = True
        self.integral_expression = None
        self.error_message = None
        self.font = pygame.font.SysFont(None, 28)
    def calculate_integral(self):        
        self.error_message = None
        self.expression_raw = self.input_box.get_text().strip()
        if not self.expression_raw:
            self.error_message = "Error: Please enter an expression."
            return       
        try:           
            self.parsed_expression = parse_function(self.expression_raw)
            self.integral_expression = integrate(self.parsed_expression, self.x)
        except Exception:
            self.integral_expression = None
            self.error_message = "Error solving integral"
    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'menu'
                if event.type==pygame.VIDEORESIZE:
                    self.WIDTH = max(720, event.w)
                    self.HEIGHT = max(406, event.h)
                    self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    self.manager.set_window_resolution((self.WIDTH, self.HEIGHT))
                    self.calculate_button.set_position((((self.WIDTH -(self.WIDTH // 3.6))//2), 160))
                    self.calculate_button.set_dimensions((self.WIDTH//3.6, 50))
                    self.input_box.set_position((((self.WIDTH -(self.WIDTH // 3.6))//2), 100))
                    self.input_box.set_dimensions((self.WIDTH // 3.6, 50))
                self.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.calculate_button:
                        self.calculate_integral()
                        if self.integral_expression is not None:                     
                            self.result_surf = return_latex_surface(convert_latex(self.integral_expression))
            self.surface.fill((255, 255, 255))
            self.manager.update(time_delta)
            self.manager.draw_ui(self.surface)
            if self.error_message:
                error_surf = self.font.render(self.error_message, True, (200, 50, 50))
                self.surface.blit(error_surf, (100, 260))
            elif self.integral_expression is not None:
                self.surface.blit(self.result_surf, (100, 260))
            pygame.display.flip()

        

        
        

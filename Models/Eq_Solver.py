import pygame
import sys
import pygame_gui
from Tools.eq_solver import solve
from Tools.convert_latex import convert_latex, return_latex_surface

class Equation_Solver :
    def __init__(self, surface, width, height):
        self.WIDTH, self.HEIGHT, self.SURFACE = width, height, surface
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((((self.WIDTH -(self.WIDTH // 2))//2), 100), (self.WIDTH // 2, 50)), 
            manager=self.manager,
            placeholder_text="Enter Equation"
        )
        self.solve_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((((self.WIDTH -(self.WIDTH // 2))//2), 160), (self.WIDTH//2, 50)),
            text="Calculate",
            manager=self.manager
        )
        self.running = True
        self.equation = None
        self.error_message = None
        self.font = pygame.font.SysFont(None, 28)
    def eq_solve(self):
        self.error_message = None
        self.equation = self.input_box.get_text().strip()
        if not self.equation:
            self.error_message = "Error: Please enter an equation."
            return        
        try:            
            self.equation = solve(self.equation)
        except Exception as e:
            self.equation = None
            self.error_message = f"Error solving equation: {str(e)}"
    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = max(720, event.w), max(406, event.h)
                    self.SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                    self.manager.set_window_resolution((self.WIDTH, self.HEIGHT))
                    self.input_box.set_position((((self.WIDTH -(self.WIDTH // 2))//2), 100))
                    self.input_box.set_dimensions((self.WIDTH // 2, 50))
                    self.solve_button.set_position((((self.WIDTH -(self.WIDTH // 2))//2), 160))
                    self.solve_button.set_dimensions((self.WIDTH//2, 50))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'menu'
                self.manager.process_events(event)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        try:
                            if event.ui_element == self.solve_button and self.input_box.get_text().strip() is not None:
                                self.eq_solve()
                                self.result_surf = return_latex_surface(convert_latex(self.equation))                        
                        except Exception as e:
                            self.error_message = str(e)                
            self.manager.update(time_delta)
            self.SURFACE.fill((255, 255, 255))
            self.manager.draw_ui(self.SURFACE)
            if self.error_message:
                error_surf = self.font.render(self.error_message, True, (200, 50, 50))
                self.SURFACE.blit(error_surf, (100, 230))
            elif self.equation is not None:
                self.SURFACE.blit(self.result_surf, (100, 230))
            pygame.display.flip()

        
import sys
from typing import Literal, Optional

import numpy as np
import pygame as pg
import pygame_gui
import sympy as sp

from tools import Plotter, parse_function


class Func:
    def __init__(self, function: list) -> None:
        self.num_functions = []
        for i in function:
            self.exp = parse_function(function_str=i)
            self.x = sp.symbols("x")
            self.function = sp.sympify(self.exp)
            self.num_function = sp.lambdify(self.x, self.function, "numpy")
            self.num_functions.append(self.num_function)


class GraphRepresentation:
    def __init__(self, surface, WIDTH: int, HEIGHT: int, CLOCK) -> None:
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.SURFACE = surface
        self.graph = Plotter(width=self.WIDTH, height=self.HEIGHT)
        self.surf_rect = pg.Rect(0, 0, self.WIDTH * 3 // 4, self.HEIGHT)
        self.CLOCK = CLOCK

        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        self.plot_button = pygame_gui.elements.UIButton(
            relative_rect=pg.Rect((self.WIDTH - 80, self.HEIGHT - 40), (80, 30)),
            text="Plot",
            manager=self.manager,
        )

        self.boxes = []
        for i in range(5):
            y_pos = 10 + i * 40
            box = pygame_gui.elements.UITextEntryLine(
                relative_rect=pg.Rect(
                    (self.WIDTH * 3 // 4 + 10, y_pos), (self.WIDTH // 4 - 10, 30)
                ),
                manager=self.manager,
                placeholder_text="Enter function",
            )
            self.boxes.append(box)

        self.surf = pg.Surface((self.surf_rect.width, self.surf_rect.height)).convert()
        self.fn = Func(["x^2"])

        self.colors = [
            (220, 20, 60),
            (30, 144, 255),
            (50, 205, 50),
            (255, 140, 0),
            (138, 43, 226),
        ]

        x_space = np.linspace(
            self.graph.l_bound, self.graph.r_bound, self.WIDTH * 3 // 4
        )
        self.matrix = [self.graph.generate_points(x_space, self.fn.num_functions[0])]
        self.running = True

    def update_functions(self):
        functions = []
        for box in self.boxes:
            text = box.get_text().strip()
            if text:
                functions.append(text)

        if not functions:
            return []

        self.fn = Func(functions)
        self.recalculate_matrix()
        return self.matrix

    def recalculate_matrix(self):
        self.matrix = []
        if not hasattr(self, "fn") or not self.fn.num_functions:
            return

        view_span = self.graph.r_bound - self.graph.l_bound
        num_points = (self.WIDTH) * 10
        x_space = np.linspace(
            self.graph.l_bound - view_span * 2,
            self.graph.r_bound + view_span * 2,
            num_points,
        )

        for func in self.fn.num_functions:
            self.matrix.append(self.graph.generate_points(x_space, func))

    def run(self) -> Optional[Literal["menu"]]:

        while self.running:
            time_delta = self.CLOCK.tick(75) / 1000.0
            time_delta = min(time_delta, 0.05)

            self.SURFACE.fill((255, 255, 255))
            self.surf.fill((255, 255, 255))

            for event in pg.event.get():
                self.manager.process_events(event)

                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = max(event.w, 720), max(event.h, 406)
                    self.graph.WIDTH, self.graph.HEIGHT = (
                        self.WIDTH * 3 // 4,
                        self.HEIGHT,
                    )
                    self.graph.draw = True
                    self.SURFACE = pg.display.set_mode(
                        (self.WIDTH, self.HEIGHT), pg.RESIZABLE
                    )
                    self.surf_rect = pg.Rect(0, 0, self.WIDTH * 3 // 4, self.HEIGHT)
                    self.surf = pg.Surface(
                        (self.surf_rect.width, self.surf_rect.height)
                    ).convert()
                    self.manager.set_window_resolution((self.WIDTH, self.HEIGHT))
                    self.plot_button.set_position((self.WIDTH - 80, self.HEIGHT - 40))
                    for index, box in enumerate(self.boxes):
                        box.set_position((self.WIDTH * 3 // 4 + 10, 10 + index * 40))
                        box.set_dimensions((self.WIDTH // 4 - 10, 30))
                    self.recalculate_matrix()

                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return "menu"

                elif event.type == pg.MOUSEMOTION:
                    self.mouse = pg.mouse.get_pressed()
                    if self.mouse[0]:
                        self.rel_x, self.rel_y = event.rel
                        self.graph.movement(event=["panning", (self.rel_x, self.rel_y)])

                elif event.type == pg.MOUSEBUTTONUP:
                    self.recalculate_matrix()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_o:
                        self.graph.movement(event=["reset"])
                        self.recalculate_matrix()

                elif event.type == pg.MOUSEWHEEL:
                    self.m_x, self.m_y = pg.mouse.get_pos()
                    if self.surf_rect.collidepoint(self.m_x, self.m_y):
                        self.graph.movement(
                            event=["zooming", (self.m_x, self.m_y), event.y]
                        )
                        self.recalculate_matrix()

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.plot_button:
                        self.matrix = self.update_functions()
                        self.graph.draw = True

            self.graph.draw_graph(surface=self.surf)

            if self.graph.draw:
                self.graph.lines = []
                for index, matrice in enumerate(self.matrix):
                    color = self.colors[index % len(self.colors)]
                    self.graph.plot(math_cords=matrice, color=color)

            self.graph.draw_points(surface=self.surf)
            self.SURFACE.blit(self.surf, self.surf_rect.topleft)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.SURFACE)
            pg.display.flip()

        pg.quit()
        sys.exit()

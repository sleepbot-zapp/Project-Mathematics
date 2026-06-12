import webbrowser
from enum import StrEnum

import pygame as pg

from models import (
    Derivative,
    EquationSolver,
    Extrema,
    GraphRepresentation,
    Integral,
    Menu,
)

WIDTH, HEIGHT = 1280, 720

screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.RESIZABLE)

pg.display.set_caption("Math Tool")

CLOCK = pg.time.Clock()


class View(StrEnum):
    MENU = "menu"
    GRAPH = "graph"
    DERIVATIVE = "derivative"
    INTEGRAL = "integral"
    EQSOLVER = "eq_solver"
    EXTREMA = "extrema"
    AGENTS = "agents"


class Engine:
    def __init__(self, view, WIDTH, HEIGHT):

        self.view = view

        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.CURRENT_VIEW = None

    def initialize_view(self):

        while True:
            self.WIDTH, self.HEIGHT = screen.get_size()

            match self.view:
                case View.MENU:
                    self.CURRENT_VIEW = Menu(
                        width=self.WIDTH, height=self.HEIGHT, surface=screen
                    )
                    self.view = self.CURRENT_VIEW.run()

                case View.GRAPH:
                    self.CURRENT_VIEW = GraphRepresentation(
                        surface=screen,
                        WIDTH=self.WIDTH,
                        HEIGHT=self.HEIGHT,
                        CLOCK=CLOCK,
                    )
                    self.view = self.CURRENT_VIEW.run()

                case View.DERIVATIVE:
                    self.CURRENT_VIEW = Derivative(
                        WIDTH=self.WIDTH, HEIGHT=self.HEIGHT, surface=screen
                    )
                    self.view = self.CURRENT_VIEW.run()

                case View.INTEGRAL:
                    self.CURRENT_VIEW = Integral(
                        WIDTH=self.WIDTH, HEIGHT=self.HEIGHT, surface=screen
                    )
                    self.view = self.CURRENT_VIEW.run()

                case View.EQSOLVER:
                    self.CURRENT_VIEW = EquationSolver(
                        surface=screen, width=self.WIDTH, height=self.HEIGHT
                    )
                    self.view = self.CURRENT_VIEW.run()

                case View.EXTREMA:
                    self.CURRENT_VIEW = Extrema(
                        surface=screen, width=self.WIDTH, height=self.HEIGHT
                    )
                    self.view = self.CURRENT_VIEW.run()

                case View.AGENTS:
                    webbrowser.open("http://localhost:8000")

                    self.CURRENT_VIEW = Menu(
                        width=self.WIDTH, height=self.HEIGHT, surface=screen
                    )
                    self.view = self.CURRENT_VIEW.run()

                case _:
                    self.view = View.MENU


if __name__ == "__main__":
    Eng = Engine("menu", 1280, 720)

    Eng.initialize_view()

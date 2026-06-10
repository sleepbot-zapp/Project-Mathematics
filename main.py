import sys
import webbrowser

import pygame as pg

from models import (
    Derivative,
    EquationSolver,
    Extrema,
    GraphRepresentation,
    Integral,
    Menu,
)

view = "menu"

WIDTH, HEIGHT = 1280, 720

screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.RESIZABLE)

pg.display.set_caption("Math Tool")

CLOCK = pg.time.Clock()


class Engine:
    def __init__(self, view, WIDTH, HEIGHT):

        self.view = view

        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.CURRENT_VIEW = None

    def initialize_view(self):

        while True:
            self.WIDTH, self.HEIGHT = screen.get_size()

            if self.view == "menu":
                self.CURRENT_VIEW = Menu(
                    width=self.WIDTH, height=self.HEIGHT, surface=screen
                )

                self.view = self.CURRENT_VIEW.run()

            if self.view == "Graph":
                self.CURRENT_VIEW = GraphRepresentation(
                    surface=screen, WIDTH=self.WIDTH, HEIGHT=self.HEIGHT, CLOCK=CLOCK
                )

                self.view = self.CURRENT_VIEW.run()

            if self.view == "Derivative":
                self.CURRENT_VIEW = Derivative(
                    WIDTH=self.WIDTH, HEIGHT=self.HEIGHT, surface=screen
                )

                self.view = self.CURRENT_VIEW.run()

            if self.view == "Integral":
                self.CURRENT_VIEW = Integral(
                    WIDTH=self.WIDTH, HEIGHT=self.HEIGHT, surface=screen
                )

                self.view = self.CURRENT_VIEW.run()

            if self.view == "Eq_Solver":
                self.CURRENT_VIEW = EquationSolver(
                    surface=screen, width=self.WIDTH, height=self.HEIGHT
                )

                self.view = self.CURRENT_VIEW.run()

            if self.view == "Extrema":
                self.CURRENT_VIEW = Extrema(
                    surface=screen, width=self.WIDTH, height=self.HEIGHT
                )

                self.view = self.CURRENT_VIEW.run()

            if self.view == "Agents":
                webbrowser.open("http://localhost:8000")

                self.CURRENT_VIEW = Menu(
                    width=self.WIDTH, height=self.HEIGHT, surface=screen
                )

                self.view = self.CURRENT_VIEW.run()


if __name__ == "__main__":
    Eng = Engine("menu", 1280, 720)

    Eng.initialize_view()

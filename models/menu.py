import sys
from pathlib import Path
from typing import Literal, Optional

import pygame as pg

pg.init()

pg.font.init()


class Menu:
    def __init__(self, width: int, height: int, surface) -> None:
        self.img_directory = (
            Path(__file__).resolve().parent.parent / "images" / "menu.png"
        ).as_posix()
        self.bg_image = pg.image.load(self.img_directory).convert_alpha()
        self.WIDTH, self.HEIGHT = width, height
        self.scaled_image = pg.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))
        self.SURFACE = surface
        self.func_lists = [
            "graph",
            "eq_solver",
            "derivative",
            "integral",
            "extrema",
            "agents",
        ]
        self.running = True
        self.total_boxes_x = self.WIDTH // 15
        self.total_boxes_y = self.HEIGHT // 12
        self.font = pg.font.SysFont("Bahnschrift", int(self.total_boxes_y // 2))
        """The screen is divided into 15 parts horizontally, They are ordered as: 1, 6(box), 1, 6(box), 1"""
        """It is divided into 12 parts vertically given 1, 1(box), 1, 1(box), 1, 1(box), 6"""
        self.cords = [
            pg.Rect(
                self.total_boxes_x,
                self.total_boxes_y,
                self.total_boxes_x * 6,
                self.total_boxes_y,
            ),
            pg.Rect(
                self.total_boxes_x * 8,
                self.total_boxes_y,
                self.total_boxes_x * 6,
                self.total_boxes_y,
            ),
            pg.Rect(
                self.total_boxes_x,
                self.total_boxes_y * 3,
                self.total_boxes_x * 6,
                self.total_boxes_y,
            ),
            pg.Rect(
                self.total_boxes_x * 8,
                self.total_boxes_y * 3,
                self.total_boxes_x * 6,
                self.total_boxes_y,
            ),
            pg.Rect(
                self.total_boxes_x,
                self.total_boxes_y * 5,
                self.total_boxes_x * 6,
                self.total_boxes_y,
            ),
            pg.Rect(
                self.total_boxes_x * 8,
                self.total_boxes_y * 5,
                self.total_boxes_x * 6,
                self.total_boxes_y,
            ),
        ]

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = max(720, event.w), max(406, event.h)
                    self.scaled_image = pg.transform.scale(
                        self.bg_image, (self.WIDTH, self.HEIGHT)
                    )
                    self.SURFACE = pg.display.set_mode(
                        (self.WIDTH, self.HEIGHT), pg.RESIZABLE
                    )
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.event_pos = pg.mouse.get_pos()
                    self.bool_index = []
                    for idx, rect in enumerate(self.cords):
                        if rect.collidepoint(self.event_pos):
                            return self.func_lists[idx]

            self.SURFACE.blit(self.scaled_image)
            for i in self.cords:
                pg.draw.rect(self.SURFACE, (255, 255, 255), i, border_radius=8)
                pg.draw.rect(self.SURFACE, (0, 0, 0), i, width=5, border_radius=8)
                text = self.font.render(
                    self.func_lists[self.cords.index(i)], True, (0, 0, 0)
                )
                text_rect = text.get_rect(center=i.center)
                self.SURFACE.blit(text, text_rect)
            pg.display.flip()

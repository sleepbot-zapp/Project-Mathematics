import numpy as np
import pygame as pg

class Plotter:
    
    def __init__(self, width: int, height: int, scale=30):
        self.WIDTH = width
        self.HEIGHT = height
        self.ORIGIN_X = width // 2
        self.ORIGIN_Y = height // 2
        self.SCALE = scale
        self.draw = True
        self.lines = []
        self.MAX_SCALE = 500
        self.MIN_SCALE = 5
        pg.font.init()
        self.font = pg.font.SysFont('segoeui', 12)


    @property
    def r_bound(self):
        return (self.WIDTH - self.ORIGIN_X + 500) / self.SCALE
    
    @property
    def l_bound(self):
        return -(self.ORIGIN_X + 500) / self.SCALE
    
    @property
    def u_bound(self):
        return (self.ORIGIN_Y + 500) / self.SCALE
    
    @property
    def d_bound(self):
        return (self.ORIGIN_Y - self.HEIGHT - 500) / self.SCALE

    def draw_graph(self, surface):
        grid_step = 5 if self.SCALE < 20 else 1
        pixel_step = self.SCALE * grid_step
        offset_x = self.ORIGIN_X % pixel_step
        offset_y = self.ORIGIN_Y % pixel_step
        y_positions = np.arange(offset_y, self.HEIGHT, pixel_step)
        x_positions = np.arange(offset_x, self.WIDTH, pixel_step)
        
        for i in x_positions:
            pg.draw.aaline(surface, (156, 156, 156), (i, 0), (i, self.HEIGHT), 1)
            math_x = (i - self.ORIGIN_X) / self.SCALE
            if abs(math_x) > 0.01: 
                text = self.font.render(f"{math_x:g}", True, (60, 60, 60))
                surface.blit(text, (i , self.HEIGHT - 25))
            
        for i in y_positions:
            pg.draw.aaline(surface, (156, 156, 156), (0, i), (self.WIDTH, i), 1)
            math_y = (self.ORIGIN_Y - i) / self.SCALE
            if abs(math_y) > 0.01:
                text = self.font.render(f"{math_y:g}", True, (60, 60, 60))
                surface.blit(text, (5, i ))
            
        pg.draw.aaline(surface, 'black', (0, self.ORIGIN_Y), (self.WIDTH, self.ORIGIN_Y), 1)
        pg.draw.aaline(surface, 'black', (self.ORIGIN_X, 0), (self.ORIGIN_X, self.HEIGHT), 1)
        
    def plot(self, math_cords: np.array, color=(255, 0, 0)):
        math_x, math_y = math_cords.T
        view_mask = (math_x > self.l_bound) & (math_x < self.r_bound) & (math_y < self.u_bound) & (math_y > self.d_bound) & np.isfinite(math_x) & np.isfinite(math_y) & ~np.isnan(math_x) & ~np.isnan(math_y)
        v_x = math_x[view_mask]
        v_y = math_y[view_mask]
        screen_x = self.ORIGIN_X + v_x * self.SCALE
        screen_y = self.ORIGIN_Y - v_y * self.SCALE
        mask = np.isfinite(screen_y)
        
        pts = np.column_stack((screen_x[mask], screen_y[mask]))
        self.lines.append((pts, color))
        self.draw = False

    def draw_points(self, surface):
        for pts, color in self.lines:
            if pts.shape[0] >= 2:
                pg.draw.aalines(surface, color, False, pts)

    def movement(self, event):
        if event[0] == 'panning':
            self.ORIGIN_X += event[1][0]
            self.ORIGIN_Y += event[1][1]
            self.draw = True

        elif event[0] == 'zooming':
            mouse_x, mouse_y = event[1][0], event[1][1]
            math_x = (mouse_x - self.ORIGIN_X) / self.SCALE 
            math_y = (self.ORIGIN_Y - mouse_y) / self.SCALE 

            if event[2] > 0:
                self.SCALE += 5
            elif event[2] < 0:
                self.SCALE -= 5

            self.SCALE = max(self.MIN_SCALE, min(self.SCALE, self.MAX_SCALE))
            self.ORIGIN_X = mouse_x - math_x * self.SCALE
            self.ORIGIN_Y = mouse_y + math_y * self.SCALE
            self.draw = True

        elif event[0] == 'reset':
            self.ORIGIN_X = self.WIDTH // 2
            self.ORIGIN_Y = self.HEIGHT // 2
            self.SCALE = 50
            self.draw = True

    def generate_points(self, math_x_range, numpy_function):
        self.num_function = numpy_function
        try:
            math_y = self.num_function(math_x_range)
            if isinstance(math_y, (int, float)):
                math_y = np.full_like(math_x_range, math_y)
            return np.column_stack((math_x_range, math_y))
        except Exception:
            math_y = np.zeros_like(math_x_range)
            return np.column_stack((math_x_range, math_y))
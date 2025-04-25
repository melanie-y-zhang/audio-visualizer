import pygame
import numpy as np
from config import WIDTH, HEIGHT

class RetroGridVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.rows = 40
        self.cols = 30 
        self.spacing = 20
        self.speed = 1
        self.wave_offset = 0 

    def draw(self, volume, fft):
        self.screen.fill((10, 0, 20))

        center_x = WIDTH // 2
        horizon = HEIGHT // 2
        self.wave_offset += 0.05 

        amplitude = max(volume * 120, 2)

        for row in range(1, self.rows):
            depth = row * self.spacing
            scale = 1 / (row * 0.1)

            height_mod = np.sin(self.wave_offset + row * 0.2) * amplitude
            y = int(horizon + height_mod + depth)

            for col in range(-self.cols, self.cols + 1):
                x = int(center_x + col * self.spacing * scale)
                pygame.draw.circle(self.screen, (255, 128, 255), (x, y), 1)

            for col in range(-self.cols, self.cols):
                x1 = int(center_x + col * self.spacing * scale)
                x2 = int(center_x + (col + 1) * self.spacing * scale)
                pygame.draw.line(self.screen, (255, 80, 255), (x1, y), (x2, y), 1)

            if row < self.rows - 1:
                next_depth = (row + 1) * self.spacing
                next_scale = 1 / ((row + 1) * 0.1)
                next_height_mod = np.sin(self.wave_offset + (row + 1) * 0.2) * amplitude
                next_y = int(horizon + next_height_mod + next_depth)

                for col in range(-self.cols, self.cols + 1, 2):
                    x1 = int(center_x + col * self.spacing * scale)
                    x2 = int(center_x + col * self.spacing * next_scale)
                    pygame.draw.line(self.screen, (180, 80, 255), (x1, y), (x2, next_y), 1)

        pygame.display.flip()
        self.clock.tick(30)

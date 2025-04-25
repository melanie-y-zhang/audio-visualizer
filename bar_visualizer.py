import pygame
import numpy as np
from config import WIDTH, HEIGHT, BAR_HEIGHT_MULTIPLIER

class BarVisualizer:
    def __init__(self, num_bars=64):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.num_bars = num_bars
        self.bar_width = WIDTH / self.num_bars
        self.bar_heights = np.zeros(self.num_bars)
        self.time = 0

    def draw(self, volume, fft):
        self.time += 0.01

        def sine_color(t, offset=0):
            return int(127 + 128 * np.sin(self.time + offset + t))

        start_color = (
            sine_color(0),
            sine_color(2),
            sine_color(4)
        )

        end_color = (
            sine_color(1),
            sine_color(3),
            sine_color(5)
        )

        self.screen.fill((0, 0, 0))

        fft = np.abs(fft[:self.num_bars])

        fft = np.where(fft > 3, fft, 0)

        fft = np.power(fft, 0.65)

        self.bar_heights = 0.9 * self.bar_heights + 0.1 * fft

        for i in range(self.num_bars):
            x = i * self.bar_width
            h = min(self.bar_heights[i] * BAR_HEIGHT_MULTIPLIER, HEIGHT)

            t = i / (self.num_bars - 1)

            color = (
                int(start_color[0] * (1 - t) + end_color[0] * t),
                int(start_color[1] * (1 - t) + end_color[1] * t),
                int(start_color[2] * (1 - t) + end_color[2] * t),
            )

            pygame.draw.rect(
                self.screen,
                color,
                (x, HEIGHT - h, self.bar_width * 0.8, h)
            )

        pygame.display.flip()
        self.clock.tick(30)

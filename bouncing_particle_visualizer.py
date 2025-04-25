import pygame
import random
import numpy as np
from config import WIDTH, HEIGHT

class BouncingParticle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.size = random.uniform(3, 7)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = (255, 255, 255)

    def move(self, volume, fft):
        speed_multiplier = 1 + volume * 5

        self.x += self.vx * speed_multiplier
        self.y += self.vy * speed_multiplier

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH:
            self.vx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.vy *= -1

        # Change color with FFT data
        if len(fft) > 5:
            r = min(int(fft[0]) % 255, 255)
            g = min(int(fft[3]) % 255, 255)
            b = min(int(fft[6]) % 255, 255)
            self.color = (r, g, b)

class BouncingParticleVisualizer:
    def __init__(self, num_particles=100):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.particles = [BouncingParticle() for _ in range(num_particles)]

    def draw(self, volume, fft):
        self.screen.fill((0, 0, 0))

        for p in self.particles:
            p.move(volume, fft)
            pygame.draw.circle(self.screen, p.color, (int(p.x), int(p.y)), int(p.size))

        pygame.display.flip()
        self.clock.tick(30)

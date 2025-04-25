import pygame
import random
import numpy as np
from config import WIDTH, HEIGHT

class RainParticle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = 0
        self.size = random.uniform(1, 5)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(2, 4)
        self.bounced = False
        self.lifetime = 500
        self.color = (
            random.randint(100, 255),
            random.randint(100, 150),
            random.randint(100, 255)
        )

    def move(self, volume, fft):
        self.x += self.vx
        self.y += self.vy

        if not self.bounced and self.y >= HEIGHT - self.size:
            self.vy = -self.vy * 0.3
            self.vx += random.uniform(-1, 1)
            self.bounced = True
        else:
            self.vy += 0.1

        if self.bounced:
            self.size *= 0.99
            self.lifetime -= 1

        # if len(fft) > 2:
        #     r = min(int(fft[1]) % 255, 255)
        #     g = min(int(fft[2]) % 255, 255)
        #     b = min(int(fft[4]) % 255, 255)
        #     self.color = (r, g, b)

    def is_dead(self):
        return self.size < 0.3 or self.lifetime <= 0


class RainParticleVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.particles = []
        self.smoothed_volume = 0 

    def draw(self, volume, fft):
        self.screen.fill((0, 0, 0))

        self.smoothed_volume = 0.8 * self.smoothed_volume + 0.2 * volume

        spawn_intensity = np.power(self.smoothed_volume, 1.4)

        num_new_particles = min(int(spawn_intensity * 10), 20)

        for _ in range(num_new_particles):
            self.particles.append(RainParticle())

        for p in self.particles:
            p.move(volume, fft)
            pygame.draw.circle(self.screen, p.color, (int(p.x), int(p.y)), int(p.size))

        self.particles = [p for p in self.particles if not p.is_dead()]

        pygame.display.flip()
        self.clock.tick(30)

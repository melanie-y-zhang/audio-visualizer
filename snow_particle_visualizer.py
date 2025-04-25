import pygame
import random
import numpy as np
from config import WIDTH, HEIGHT

class SnowParticle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = 0
        self.size = random.uniform(2.5, 5)
        self.vx = random.uniform(-0.2, 0.2)
        self.vy = random.uniform(1, 2)
        self.color = (255, 255, 255)
        self.settled = False
    def move(self, column_heights):
        if not self.settled:
            self.x += self.vx
            self.y += self.vy

            x_index = min(max(int(self.x), 0), WIDTH - 1)

            if self.y >= column_heights[x_index] - self.size:

                search_range = 2

                while True:
                    best_x = x_index
                    best_height = column_heights[x_index]

                    for dx in [-1, 1]:
                        nx = x_index + dx
                        if 0 <= nx < WIDTH:
                            if column_heights[nx] < best_height:
                                best_x = nx
                                best_height = column_heights[nx]

                    if best_x != x_index:
                        x_index = best_x
                    else:
                        break 

                self.x = x_index
                self.y = column_heights[x_index] - self.size
                column_heights[x_index] -= self.size
                self.settled = True



class SnowParticleVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.falling_particles = []
        self.settled_particles = []
        self.smoothed_volume = 0

        self.column_heights = np.full(WIDTH, HEIGHT, dtype=float)

    def draw(self, volume, fft):
        self.screen.fill((0, 0, 0))

        self.smoothed_volume = 0.85 * self.smoothed_volume + 0.15 * volume

        spawn_intensity = np.power(self.smoothed_volume, 1.5)  # was 2.0

        num_new_particles = min(int(spawn_intensity * 8), 20)  # was *4, cap 10

        if random.random() < 0.05:
            num_new_particles = max(num_new_particles, 1)

        for _ in range(num_new_particles):
            self.falling_particles.append(SnowParticle())

        for p in self.falling_particles:
            p.move(self.column_heights)
            pygame.draw.circle(self.screen, p.color, (int(p.x), int(p.y)), int(p.size))

        # Handle settled particles
        new_falling = []
        for p in self.falling_particles:
            if p.settled:
                self.settled_particles.append(p)
            else:
                new_falling.append(p)
        self.falling_particles = new_falling

        # Draw settled snow
        for p in self.settled_particles:
            pygame.draw.circle(self.screen, p.color, (int(p.x), int(p.y)), int(p.size))

        pygame.display.flip()
        self.clock.tick(30)

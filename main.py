import pygame
from audio_input import AudioInput

from rain_particle_visualizer import RainParticleVisualizer
from snow_particle_visualizer import SnowParticleVisualizer
from bar_visualizer import BarVisualizer
from retro_grid_visualizer import RetroGridVisualizer
from bouncing_particle_visualizer import BouncingParticleVisualizer

VISUALIZERS = [
    RainParticleVisualizer,
    RetroGridVisualizer,
    # SnowParticleVisualizer,
    BarVisualizer,
    BouncingParticleVisualizer
]

def main():
    pygame.init()

    visualizer_index = 0
    visualizer = VISUALIZERS[visualizer_index]()  # create first visualizer
    audio = AudioInput()
    audio.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Toggle visualizer
                    visualizer_index = (visualizer_index + 1) % len(VISUALIZERS)
                    visualizer = VISUALIZERS[visualizer_index]()
                    print(f"Switched to: {visualizer.__class__.__name__}")

        visualizer.draw(audio.volume, audio.fft)

    audio.stop()
    pygame.quit()

if __name__ == "__main__":
    main()

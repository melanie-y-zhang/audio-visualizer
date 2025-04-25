import numpy as np
import sounddevice as sd
from config import SAMPLE_RATE, BUFFER_SIZE

class AudioInput:

    # print(sd.query_devices())
    def __init__(self):
        self.volume = 0
        self.fft = np.zeros(BUFFER_SIZE)

        self.stream = sd.InputStream(
            device =0,
            channels=1,
            callback=self.audio_callback,
            blocksize=BUFFER_SIZE,
            samplerate=SAMPLE_RATE
        )

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def audio_callback(self, indata, frames, time, status):
        audio_data = np.squeeze(indata)
        self.volume = np.linalg.norm(audio_data)

        fft_raw = np.abs(np.fft.rfft(audio_data))

        fft_scaled = fft_raw * 1000  

        fft_scaled = np.power(fft_scaled, 1.4)

        self.fft = fft_scaled




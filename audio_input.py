import numpy as np
import sounddevice as sd
from config import SAMPLE_RATE, BUFFER_SIZE

class AudioInput:

    # print(sd.query_devices())
    def __init__(self):
        self.stream = None
        self.volume = 0
        self.fft = np.zeros(BUFFER_SIZE)

        self.device_index = self.find_usb_mic()

        device_info = sd.query_devices(self.device_index)
        input_channels = device_info['max_input_channels']

        self.stream = sd.InputStream(
            device =self.device_index,
            channels=min(2, input_channels),
            callback=self.audio_callback,
            blocksize=BUFFER_SIZE,
            samplerate=SAMPLE_RATE
        )
    def find_usb_mic(self):
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            name = dev['name'].lower()
            if 'usb' in name and dev['max_input_channels'] > 0:
                print(f"Using USB mic: {dev['name']} (device {i})")
                return i
        print("No USB mic found, using default input device.")
        return sd.default.device[0]

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def audio_callback(self, indata, frames, time, status):
        mono_data = np.mean(indata, axis=1)
        self.volume = np.linalg.norm(mono_data) / len(mono_data)
        self.fft = np.abs(np.fft.rfft(mono_data))

        fft_raw = np.abs(np.fft.rfft(mono))

        fft_scaled = fft_raw * 1000  

        fft_scaled = np.power(fft_scaled, 1.4)

        self.fft = fft_scaled

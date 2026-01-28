import numpy as np
from scipy.io import wavfile

def save_wav(filename: str, data: np.ndarray, sample_rate: int = 44100):
    scaled = np.int16(data * 32767)
    wavfile.write(filename, sample_rate, scaled)

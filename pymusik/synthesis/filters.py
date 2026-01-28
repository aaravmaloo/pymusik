import numpy as np
from scipy import signal

class Filter:
    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        return data

class LowPassFilter(Filter):
    def __init__(self, cutoff: float = 1000.0, resonance: float = 1.0):
        self.cutoff = cutoff
        self.resonance = resonance

    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        if self.cutoff >= sample_rate / 2:
            return data
            
        nyquist = 0.5 * sample_rate
        normal_cutoff = self.cutoff / nyquist
        
        b, a = signal.butter(2, normal_cutoff, btype='low', analog=False)
        return signal.lfilter(b, a, data)

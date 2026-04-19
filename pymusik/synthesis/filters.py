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

class HighPassFilter(Filter):
    def __init__(self, cutoff: float = 100.0, resonance: float = 1.0):
        self.cutoff = cutoff
        self.resonance = resonance

    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        if self.cutoff >= sample_rate / 2:
            return data

        nyquist = 0.5 * sample_rate
        normal_cutoff = self.cutoff / nyquist

        b, a = signal.butter(2, normal_cutoff, btype='high', analog=False)
        return signal.lfilter(b, a, data)

class BandPassFilter(Filter):
    def __init__(self, low_cutoff: float = 500.0, high_cutoff: float = 2000.0, resonance: float = 1.0):
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.resonance = resonance

    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        nyquist = 0.5 * sample_rate
        low = self.low_cutoff / nyquist
        high = self.high_cutoff / nyquist

        if low <= 0 or high >= 1 or low >= high:
            return data

        b, a = signal.butter(2, [low, high], btype='band', analog=False)
        return signal.lfilter(b, a, data)

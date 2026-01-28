import numpy as np
from abc import ABC, abstractmethod

class Oscillator(ABC):
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.phase = 0.0

    @abstractmethod
    def generate(self, freq: float, duration_samples: int) -> np.ndarray:
        pass

class SineOscillator(Oscillator):
    def generate(self, freq: float, duration_samples: int) -> np.ndarray:
        t = np.arange(duration_samples) / self.sample_rate
        phases = 2 * np.pi * freq * t + self.phase
        output = np.sin(phases)
        self.phase = phases[-1] % (2 * np.pi) if len(phases) > 0 else self.phase
        return output

class SawtoothOscillator(Oscillator):
    def generate(self, freq: float, duration_samples: int) -> np.ndarray:
        t = np.arange(duration_samples) / self.sample_rate
        phases = 2 * freq * t + (self.phase / np.pi)
        output = 2 * (phases % 2) - 1
        self.phase = (phases[-1] % 2) * np.pi if len(phases) > 0 else self.phase
        return output

class SquareOscillator(Oscillator):
    def __init__(self, sample_rate: int = 44100, duty_cycle: float = 0.5):
        super().__init__(sample_rate)
        self.duty_cycle = duty_cycle

    def generate(self, freq: float, duration_samples: int) -> np.ndarray:
        t = np.arange(duration_samples) / self.sample_rate
        phases = freq * t + (self.phase / (2 * np.pi))
        output = np.where((phases % 1) < self.duty_cycle, 1.0, -1.0)
        self.phase = (phases[-1] % 1) * 2 * np.pi if len(phases) > 0 else self.phase
        return output

class NoiseOscillator(Oscillator):
    def generate(self, freq: float, duration_samples: int) -> np.ndarray:
        return np.random.uniform(-1, 1, duration_samples)

import numpy as np
from scipy import signal

class Distortion:
    def __init__(self, drive: float = 1.0, type: str = "soft"):
        self.drive = drive
        self.type = type

    def process(self, data: np.ndarray) -> np.ndarray:
        driven = data * self.drive
        if self.type == "soft":
            return np.tanh(driven)
        else:
            return np.clip(driven, -1.0, 1.0)

class Reverb:
    def __init__(self, room_size: float = 0.5, damping: float = 0.5):
        self.room_size = room_size
        self.damping = damping

    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        delay_samples = int(0.05 * sample_rate)
        if len(data) <= delay_samples: return data
        out = np.copy(data)
        out[delay_samples:] += data[:-delay_samples] * self.room_size
        return out / (1.0 + self.room_size)

class Delay:
    def __init__(self, time: float = 0.3, feedback: float = 0.4, mix: float = 0.3):
        self.time = time
        self.feedback = feedback
        self.mix = mix

    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        d_samples = int(self.time * sample_rate)
        if d_samples <= 0 or d_samples >= len(data): return data
        out = np.copy(data)
        for i in range(d_samples, len(data)):
            out[i] = (1 - self.mix) * data[i] + self.mix * out[i-d_samples] * self.feedback
        return out

class Chorus:
    def __init__(self, rate: float = 1.5, depth: float = 0.002, mix: float = 0.5):
        self.rate = rate
        self.depth = depth
        self.mix = mix

    def process(self, data: np.ndarray, sample_rate: int) -> np.ndarray:
        t = np.arange(len(data)) / sample_rate
        offset = (self.depth * sample_rate * np.sin(2 * np.pi * self.rate * t)).astype(int)
        out = np.copy(data)
        for i in range(len(data)):
            idx = i + offset[i]
            if 0 <= idx < len(data):
                out[i] = (1 - self.mix) * data[i] + self.mix * data[idx]
        return out

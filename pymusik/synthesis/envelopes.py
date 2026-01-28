import numpy as np

class Envelope:
    def apply(self, signal: np.ndarray, sample_rate: int) -> np.ndarray:
        return signal * self.generate(len(signal), sample_rate)

class ADSREnvelope(Envelope):
    def __init__(self, attack: float = 0.01, decay: float = 0.1, sustain: float = 0.5, release: float = 0.2):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

    def generate(self, duration_samples: int, sample_rate: int) -> np.ndarray:
        a_samples = int(self.attack * sample_rate)
        d_samples = int(self.decay * sample_rate)
        r_samples = int(self.release * sample_rate)
        
        env = np.ones(duration_samples)
        
        if a_samples > 0:
            a_curve = np.linspace(0, 1, min(a_samples, duration_samples))
            env[:len(a_curve)] = a_curve
            
        if d_samples > 0 and len(env) > a_samples:
            d_end = min(a_samples + d_samples, duration_samples)
            d_curve = np.linspace(1, self.sustain, d_end - a_samples)
            env[a_samples:d_end] = d_curve
            
        if len(env) > a_samples + d_samples:
            env[a_samples + d_samples:] = self.sustain
            
        if r_samples > 0 and duration_samples > r_samples:
            r_curve = np.linspace(self.sustain, 0, r_samples)
            env[-r_samples:] = r_curve
        elif r_samples > 0:
            r_curve = np.linspace(self.sustain, 0, duration_samples)
            env = r_curve

        return env

    def get_curve(self, duration_samples: int, sample_rate: int) -> np.ndarray:
        return self.generate(duration_samples, sample_rate)

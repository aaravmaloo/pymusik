from typing import Tuple

class TimeContext:
    def __init__(self, bpm: float = 120.0, time_signature: Tuple[int, int] = (4, 4), sample_rate: int = 44100):
        self.bpm = bpm
        self.time_signature = time_signature
        self.sample_rate = sample_rate
        
    @property
    def seconds_per_beat(self) -> float:
        return 60.0 / self.bpm
    
    def beats_to_samples(self, beats: float) -> int:
        return int(beats * self.seconds_per_beat * self.sample_rate)
    
    def samples_to_beats(self, samples: int) -> float:
        return samples / (self.sample_rate * self.seconds_per_beat)

    def __repr__(self):
        return f"TimeContext(bpm={self.bpm}, ts={self.time_signature}, sr={self.sample_rate})"

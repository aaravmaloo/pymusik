import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent

class PianoInstrument(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.995

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        duration_samples = time_context.beats_to_samples(note_event.note.duration)
        if duration_samples <= 0:
            return np.array([])
            
        freq = note_event.note.pitch.frequency
        if freq <= 0:
            return np.zeros(duration_samples)
            
        L = int(self.sample_rate / freq)
        if L <= 0:
            return np.zeros(duration_samples)
            
        ring_buffer = np.random.uniform(-1, 1, L)
        output = np.zeros(duration_samples)
        
        for i in range(duration_samples):
            output[i] = ring_buffer[0]
            new_sample = 0.5 * (ring_buffer[0] + ring_buffer[1]) * self.damping
            ring_buffer = np.roll(ring_buffer, -1)
            ring_buffer[-1] = new_sample
            
        output *= note_event.note.velocity
        fade_samples = min(100, duration_samples)
        output[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return output

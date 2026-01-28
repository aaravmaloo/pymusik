import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.oscillators import SineOscillator, SquareOscillator
from ..effects.distortion import Distortion

class PhonkCowbell(Instrument):
    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency
        
        sig = 0.6 * np.sign(np.sin(2 * np.pi * f * t))
        sig += 0.4 * np.sign(np.sin(2 * np.pi * f * 1.503 * t))
        
        env = np.exp(-t * 15)
        
        pitch_env = 1.0 + 0.1 * np.exp(-t * 50)
        phase = 2 * np.pi * f * np.cumsum(pitch_env) / self.sample_rate
        sig = np.sign(np.sin(phase))
        
        return sig * env * note_event.note.velocity

class Bass808(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.dist = Distortion(drive=10.0, type="soft")

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency
        
        punch_env = 2.0 * np.exp(-t * 40)
        phase = 2 * np.pi * f * (t + np.cumsum(punch_env) / self.sample_rate)
        sub = np.sin(phase)
        
        grit = 0.3 * np.sin(3 * phase) * np.exp(-t * 5)
        
        sig = sub + grit
        
        env = np.exp(-t * 1.5)
        sig = sig * env
        
        sig = self.dist.process(sig)
        sig = sig * 0.9
        
        return sig * note_event.note.velocity

import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.oscillators import SineOscillator, NoiseOscillator
from ..synthesis.envelopes import ADSREnvelope

class DrumInstrument(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        note_name = note_event.note.pitch.name
        
        if "C" in note_name:
            return self._generate_kick(note_event, time_context)
        elif "D" in note_name:
            return self._generate_snare(note_event, time_context)
        elif "F" in note_name:
            return self._generate_hihat(note_event, time_context)
        else:
            return self._generate_kick(note_event, time_context)

    def _generate_kick(self, event, ctx) -> np.ndarray:
        samples = ctx.beats_to_samples(event.note.duration)
        t = np.arange(samples) / self.sample_rate
        freq = 40 + 110 * np.exp(-t * 30)
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        out = np.sin(phase)
        env = np.exp(-t * 15)
        return out * env * event.note.velocity

    def _generate_snare(self, event, ctx) -> np.ndarray:
        samples = ctx.beats_to_samples(event.note.duration)
        t = np.arange(samples) / self.sample_rate
        body = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 20)
        noise = np.random.uniform(-1, 1, samples) * np.exp(-t * 15)
        out = 0.4 * body + 0.6 * noise
        return out * event.note.velocity

    def _generate_hihat(self, event, ctx) -> np.ndarray:
        samples = ctx.beats_to_samples(event.note.duration)
        t = np.arange(samples) / self.sample_rate
        noise = np.random.uniform(-1, 1, samples)
        env = np.exp(-t * 100)
        return noise * env * event.note.velocity
drum_elements = {
    "kick": 36,
    "snare": 38,
    "hihat": 42
}

import numpy as np
from .base import Instrument
from ..synthesis.oscillators import SawtoothOscillator, SineOscillator, NoiseOscillator
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter
from ..core.time import TimeContext
from ..core.events import NoteEvent

class AcidBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.osc = SawtoothOscillator(sample_rate)
        self.amp_env = ADSREnvelope(attack=0.005, decay=0.2, sustain=0.4, release=0.1)
        self.filter_env = ADSREnvelope(attack=0.01, decay=0.3, sustain=0.1, release=0.2)
        
    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        freq = note_event.note.pitch.frequency
        sig = self.osc.generate(freq, samples)
        
        # Resonant filter sweep
        f_env = self.filter_env.get_curve(samples, self.sample_rate)
        # Map 0-1 env to 300Hz-5000Hz
        cutoff_curve = 300 + 4700 * f_env
        
        # Apply filter sample-by-sample for sweeping (simple approximation)
        # Since we don't have a time-varying filter yet, we'll do it in chunks
        chunk_size = 128
        for i in range(0, samples, chunk_size):
            end = min(i + chunk_size, samples)
            cutoff = cutoff_curve[i]
            lpf = LowPassFilter(cutoff=cutoff)
            sig[i:end] = lpf.process(sig[i:end], self.sample_rate)
            
        sig = self.amp_env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.8

class ProDrums(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        
    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        note = note_event.note.pitch.name
        if "C" in note: return self._kick(note_event, time_context)
        if "D" in note: return self._snare(note_event, time_context)
        if "F" in note: return self._hat(note_event, time_context)
        return self._kick(note_event, time_context)

    def _kick(self, e, ctx):
        samples = ctx.beats_to_samples(e.note.duration)
        t = np.arange(samples) / self.sample_rate
        f = 55 + 150 * np.exp(-t * 50)
        phase = 2 * np.pi * np.cumsum(f) / self.sample_rate
        out = np.sin(phase) * np.exp(-t * 8)
        # Distortion for Hifi/Techno punch
        out = np.tanh(out * 1.5)
        return out * e.note.velocity

    def _snare(self, e, ctx):
        samples = ctx.beats_to_samples(e.note.duration)
        t = np.arange(samples) / self.sample_rate
        body = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30)
        noise = np.random.uniform(-1, 1, samples) * np.exp(-t * 20)
        out = (0.3 * body + 0.7 * noise)
        return np.tanh(out * 1.2) * e.note.velocity

    def _hat(self, e, ctx):
        samples = ctx.beats_to_samples(e.note.duration)
        noise = np.random.uniform(-1, 1, samples)
        t = np.arange(samples) / self.sample_rate
        env = np.exp(-t * 80)
        return noise * env * e.note.velocity * 0.4

class SuperSawLead(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.oscs = [SawtoothOscillator(sample_rate) for _ in range(7)]
        self.env = ADSREnvelope(attack=0.01, decay=0.1, sustain=0.4, release=0.1)
        self.lpf = LowPassFilter(cutoff=4000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        f = note_event.note.pitch.frequency
        # Detuned stack for that huge dance sound
        detunes = [1.0, 1.005, 0.995, 1.01, 0.99, 1.02, 0.98]
        sig = np.zeros(samples)
        for i, d in enumerate(detunes):
            sig += self.oscs[i].generate(f * d, samples)
            
        sig = self.env.apply(sig / 7, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity

class HyperPluck(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.001, decay=0.05, sustain=0.0, release=0.05)
        
    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency
        # Sine + high harmonic for a "clicky" pluck
        sig = 0.7 * np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t)
        sig = self.env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity

import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.oscillators import SineOscillator, SawtoothOscillator, NoiseOscillator
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter

class GuitarInstrument(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.98
        self.lpf = LowPassFilter(cutoff=1500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        freq = note_event.note.pitch.frequency
        if freq <= 0: return np.zeros(samples)
        
        L = int(self.sample_rate / freq)
        if L <= 1: return np.zeros(samples)
        
        ring_buffer = np.random.uniform(-1, 1, L)
        output = np.zeros(samples)
        
        for i in range(samples):
            output[i] = ring_buffer[0]
            avg = 0.5 * (ring_buffer[0] + ring_buffer[1])
            new_sample = avg * self.damping
            ring_buffer = np.roll(ring_buffer, -1)
            ring_buffer[-1] = new_sample
            
        output *= note_event.note.velocity
        output = self.lpf.process(output, self.sample_rate)
        fade = min(200, samples)
        output[-fade:] *= np.linspace(1, 0, fade)
        
        return output

class SaxInstrument(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.2, decay=0.2, sustain=0.6, release=0.2)
        self.lpf = LowPassFilter(cutoff=1200)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency
        
        vibrato = 1.0 + 0.005 * np.sin(2 * np.pi * 5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate
        
        sig = 0.7 * np.sin(phase) + 0.2 * np.sin(2 * phase) + 0.1 * np.sin(3 * phase)
        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        
        return sig * note_event.note.velocity

class VinylEffect(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.noise_gen = NoiseOscillator(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        noise = self.noise_gen.generate(0, samples) * 0.02
        
        for _ in range(int(samples / 10000)):
            pos = np.random.randint(0, samples)
            pop_len = np.random.randint(5, 15)
            if pos + pop_len < samples:
                noise[pos:pos+pop_len] += 0.1
                
        return noise

class MellowPiano(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.1, decay=0.3, sustain=0.4, release=0.3)
        self.lpf = LowPassFilter(cutoff=450)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0: return np.array([])
        
        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency
        
        # Sine + Triangle blend for Rhodes-ish feel
        sine = np.sin(2 * np.pi * f * t)
        tri = 2 * np.abs(2 * (f * t % 1) - 1) - 1
        sig = 0.8 * sine + 0.2 * tri
        
        # Subtle tremolo
        tremolo = 1.0 + 0.1 * np.sin(2 * np.pi * 3 * t)
        sig *= tremolo
        
        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        
        return sig * note_event.note.velocity

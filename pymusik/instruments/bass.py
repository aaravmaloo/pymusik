import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter
from ..synthesis.oscillators import SawtoothOscillator, SineOscillator


class FretlessBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.01, decay=0.15, sustain=0.5, release=0.1)
        self.lpf = LowPassFilter(cutoff=1200)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        glide = 1.0 + 0.02 * np.exp(-t * 20)
        phase = 2 * np.pi * f * np.cumsum(glide) / self.sample_rate

        sig = 0.7 * np.sin(phase)
        sig += 0.2 * np.sin(2 * phase)
        sig += 0.1 * np.sin(3 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.75


class UprightBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.993
        self.lpf = LowPassFilter(cutoff=800)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        freq = note_event.note.pitch.frequency
        if freq <= 0:
            return np.zeros(samples)

        L = int(self.sample_rate / freq)
        if L <= 1:
            return np.zeros(samples)

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
        fade = min(300, samples)
        output[-fade:] *= np.linspace(1, 0, fade)

        return output * 0.7


class SubBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.005, decay=0.1, sustain=0.7, release=0.1)
        self.lpf = LowPassFilter(cutoff=300)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = np.sin(2 * np.pi * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 2 * f * t)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.9


class WobbleBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.005, decay=0.1, sustain=0.6, release=0.1)
        self.osc = SawtoothOscillator(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = self.osc.generate(f, samples)

        wobble_rate = 4.0
        wobble_depth = 3000
        lfo = np.sin(2 * np.pi * wobble_rate * t)
        cutoff_curve = 500 + wobble_depth * (0.5 + 0.5 * lfo)

        chunk_size = 128
        for i in range(0, samples, chunk_size):
            end = min(i + chunk_size, samples)
            cutoff = cutoff_curve[i]
            lpf = LowPassFilter(cutoff=cutoff)
            sig[i:end] = lpf.process(sig[i:end], self.sample_rate)

        sig = self.env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.7

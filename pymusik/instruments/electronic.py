import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter
from ..synthesis.oscillators import SawtoothOscillator, SineOscillator, SquareOscillator
from ..effects.distortion import Distortion


class TB303(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.osc = SawtoothOscillator(sample_rate)
        self.amp_env = ADSREnvelope(attack=0.002, decay=0.15, sustain=0.0, release=0.05)
        self.filter_env = ADSREnvelope(attack=0.005, decay=0.2, sustain=0.05, release=0.15)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        freq = note_event.note.pitch.frequency
        sig = self.osc.generate(freq, samples)

        f_env = self.filter_env.get_curve(samples, self.sample_rate)
        cutoff_curve = 200 + 4800 * f_env

        chunk_size = 128
        for i in range(0, samples, chunk_size):
            end = min(i + chunk_size, samples)
            cutoff = cutoff_curve[i]
            lpf = LowPassFilter(cutoff=cutoff)
            sig[i:end] = lpf.process(sig[i:end], self.sample_rate)

        sig = self.amp_env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.7


class SupersawPad(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.oscs = [SawtoothOscillator(sample_rate) for _ in range(7)]
        self.env = ADSREnvelope(attack=0.8, decay=0.5, sustain=0.7, release=1.0)
        self.lpf = LowPassFilter(cutoff=3000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        f = note_event.note.pitch.frequency
        detunes = [1.0, 1.007, 0.993, 1.014, 0.986, 1.021, 0.979]
        sig = np.zeros(samples)
        for i, d in enumerate(detunes):
            sig += self.oscs[i].generate(f * d, samples)

        sig = self.env.apply(sig / 7, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5


class WavetableLead(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.01, decay=0.1, sustain=0.5, release=0.1)
        self.lpf = LowPassFilter(cutoff=5000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        phase = 2 * np.pi * f * t
        morph = 0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)

        sine = np.sin(phase)
        saw = 2 * (f * t % 1) - 1
        sig = (1 - morph) * sine + morph * saw

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.6


class FMBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.005, decay=0.15, sustain=0.4, release=0.08)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        mod_idx_env = 3.0 * np.exp(-t * 10)
        modulator = np.sin(2 * np.pi * f * 2 * t)
        carrier = np.sin(2 * np.pi * f * t + mod_idx_env * modulator)

        sig = self.env.apply(carrier, self.sample_rate)
        return sig * note_event.note.velocity * 0.7


class TranceGate(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.osc = SawtoothOscillator(sample_rate)
        self.env = ADSREnvelope(attack=0.001, decay=0.05, sustain=0.3, release=0.02)
        self.lpf = LowPassFilter(cutoff=4000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        f = note_event.note.pitch.frequency
        sig = self.osc.generate(f, samples)

        t = np.arange(samples) / self.sample_rate
        gate_rate = 8.0
        gate = np.where(np.sin(2 * np.pi * gate_rate * t) > 0, 1.0, 0.0)
        sig *= gate

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5


class ChiptuneLead(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.001, decay=0.05, sustain=0.6, release=0.02)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        duty = 0.25 + 0.15 * np.sin(2 * np.pi * 2.0 * t)
        phase = f * t
        sig = np.where((phase % 1) < duty, 1.0, -1.0)

        sig = self.env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.4


class ChiptuneBass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.001, decay=0.08, sustain=0.5, release=0.02)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        phase = 2 * f * t
        sig = 2 * (phase % 2) - 1

        sig = self.env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.45

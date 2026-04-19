import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, BandPassFilter


class Clavinet(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.001, decay=0.15, sustain=0.1, release=0.05)
        self.bpf = BandPassFilter(low_cutoff=500, high_cutoff=4000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.7 * np.sin(2 * np.pi * f * t)
        sig += 0.2 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 3 * f * t)

        pluck = np.random.uniform(-1, 1, samples) * np.exp(-t * 50) * 0.3
        sig += pluck

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.6


class Celesta(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.6 * np.sin(2 * np.pi * f * t)
        sig += 0.25 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.05 * np.sin(2 * np.pi * 4 * f * t)

        env = np.exp(-t * 8)
        sig *= env

        return sig * note_event.note.velocity * 0.45


class Glockenspiel(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.5 * np.sin(2 * np.pi * f * t)
        sig += 0.3 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.15 * np.sin(2 * np.pi * 5 * f * t)
        sig += 0.05 * np.sin(2 * np.pi * 7 * f * t)

        env = np.exp(-t * 5)
        sig *= env

        return sig * note_event.note.velocity * 0.4


class MusicBox(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.65 * np.sin(2 * np.pi * f * t)
        sig += 0.2 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.05 * np.sin(2 * np.pi * 5 * f * t)

        env = np.exp(-t * 6)
        sig *= env

        tine = np.random.uniform(-1, 1, samples) * np.exp(-t * 30) * 0.1
        sig += tine

        return sig * note_event.note.velocity * 0.4


class Rhodes(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.05, decay=0.3, sustain=0.4, release=0.3)
        self.lpf = LowPassFilter(cutoff=500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sine = np.sin(2 * np.pi * f * t)
        tri = 2 * np.abs(2 * (f * t % 1) - 1) - 1
        sig = 0.7 * sine + 0.3 * tri

        bell = 0.15 * np.sin(2 * np.pi * f * 6 * t) * np.exp(-t * 10)
        sig += bell

        tremolo = 1.0 + 0.08 * np.sin(2 * np.pi * 3.5 * t)
        sig *= tremolo

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.55

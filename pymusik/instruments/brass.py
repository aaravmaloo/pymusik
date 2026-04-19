import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, BandPassFilter


class Trumpet(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.05, decay=0.1, sustain=0.7, release=0.15)
        self.bpf = BandPassFilter(low_cutoff=400, high_cutoff=6000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.5 * np.sin(2 * np.pi * f * t)
        sig += 0.3 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.15 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.05 * np.sin(2 * np.pi * 4 * f * t)

        breath_noise = np.random.uniform(-1, 1, samples) * 0.03
        sig += breath_noise

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.7


class Trombone(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.08, decay=0.15, sustain=0.65, release=0.2)
        self.bpf = BandPassFilter(low_cutoff=200, high_cutoff=4000)

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

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.75


class FrenchHorn(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.12, decay=0.2, sustain=0.6, release=0.3)
        self.lpf = LowPassFilter(cutoff=2500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.7 * np.sin(2 * np.pi * f * t)
        sig += 0.2 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.07 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.03 * np.sin(2 * np.pi * 4 * f * t)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.6


class Tuba(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.1, decay=0.2, sustain=0.55, release=0.3)
        self.lpf = LowPassFilter(cutoff=1500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.75 * np.sin(2 * np.pi * f * t)
        sig += 0.15 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.07 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.03 * np.sin(2 * np.pi * 5 * f * t)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.85

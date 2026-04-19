import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, BandPassFilter, HighPassFilter


class Flute(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.12, decay=0.1, sustain=0.7, release=0.2)
        self.bpf = BandPassFilter(low_cutoff=600, high_cutoff=8000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.005 * np.sin(2 * np.pi * 5.0 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.8 * np.sin(phase)
        sig += 0.12 * np.sin(2 * phase)
        sig += 0.05 * np.sin(3 * phase)
        sig += 0.03 * np.sin(5 * phase)

        breath = np.random.uniform(-1, 1, samples) * 0.04
        sig += breath

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.55


class Piccolo(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.08, decay=0.08, sustain=0.65, release=0.15)
        self.hpf = HighPassFilter(cutoff=800)
        self.lpf = LowPassFilter(cutoff=12000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.004 * np.sin(2 * np.pi * 6.0 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.85 * np.sin(phase)
        sig += 0.1 * np.sin(2 * phase)
        sig += 0.05 * np.sin(3 * phase)

        breath = np.random.uniform(-1, 1, samples) * 0.02
        sig += breath

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.hpf.process(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5


class Clarinet(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.06, decay=0.12, sustain=0.65, release=0.15)
        self.bpf = BandPassFilter(low_cutoff=300, high_cutoff=5000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        phase = 2 * np.pi * f * t
        sig = 0.6 * np.sin(phase)
        sig += 0.25 * np.sin(3 * phase)
        sig += 0.1 * np.sin(5 * phase)
        sig += 0.05 * np.sin(7 * phase)

        vibrato = 1.0 + 0.003 * np.sin(2 * np.pi * 4.5 * t)
        sig *= vibrato

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.6


class Oboe(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.05, decay=0.1, sustain=0.6, release=0.12)
        self.bpf = BandPassFilter(low_cutoff=400, high_cutoff=6000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        phase = 2 * np.pi * f * t
        sig = 0.5 * np.sin(phase)
        sig += 0.3 * np.sin(2 * phase)
        sig += 0.12 * np.sin(3 * phase)
        sig += 0.05 * np.sin(4 * phase)
        sig += 0.03 * np.sin(5 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.55


class Bassoon(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.1, decay=0.15, sustain=0.55, release=0.2)
        self.lpf = LowPassFilter(cutoff=2500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        phase = 2 * np.pi * f * t
        sig = 0.65 * np.sin(phase)
        sig += 0.2 * np.sin(2 * phase)
        sig += 0.08 * np.sin(3 * phase)
        sig += 0.04 * np.sin(5 * phase)
        sig += 0.03 * np.sin(7 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.7


class Recorder(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.08, decay=0.1, sustain=0.6, release=0.15)
        self.lpf = LowPassFilter(cutoff=4000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        phase = 2 * np.pi * f * t
        sig = 0.75 * np.sin(phase)
        sig += 0.15 * np.sin(2 * phase)
        sig += 0.07 * np.sin(3 * phase)
        sig += 0.03 * np.sin(4 * phase)

        breath = np.random.uniform(-1, 1, samples) * 0.05
        sig += breath

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5

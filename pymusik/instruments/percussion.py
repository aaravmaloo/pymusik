import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, BandPassFilter, HighPassFilter


class Timpani(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        pitch_env = 1.0 + 0.05 * np.exp(-t * 40)
        phase = 2 * np.pi * f * np.cumsum(pitch_env) / self.sample_rate
        sig = np.sin(phase)

        sig += 0.3 * np.sin(2 * phase) * np.exp(-t * 8)
        sig += 0.1 * np.sin(3 * phase) * np.exp(-t * 12)

        env = np.exp(-t * 4)
        sig *= env

        noise = np.random.uniform(-1, 1, samples) * np.exp(-t * 30) * 0.1
        sig += noise

        return sig * note_event.note.velocity * 0.8


class Marimba(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.7 * np.sin(2 * np.pi * f * t)
        sig += 0.2 * np.sin(2 * np.pi * 4 * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 10 * f * t)

        env = np.exp(-t * 6)
        sig *= env

        return sig * note_event.note.velocity * 0.6


class Xylophone(Instrument):
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
        sig += 0.15 * np.sin(2 * np.pi * 6 * f * t)
        sig += 0.05 * np.sin(2 * np.pi * 10 * f * t)

        env = np.exp(-t * 12)
        sig *= env

        return sig * note_event.note.velocity * 0.55


class Vibraphone(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.6 * np.sin(2 * np.pi * f * t)
        sig += 0.25 * np.sin(2 * np.pi * 4 * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 10 * f * t)

        tremolo = 1.0 + 0.3 * np.sin(2 * np.pi * 2.0 * t)
        sig *= tremolo

        env = np.exp(-t * 2)
        sig *= env

        return sig * note_event.note.velocity * 0.5


class Gong(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.4 * np.sin(2 * np.pi * f * t)
        sig += 0.25 * np.sin(2 * np.pi * f * 1.5 * t)
        sig += 0.2 * np.sin(2 * np.pi * f * 2.0 * t)
        sig += 0.1 * np.sin(2 * np.pi * f * 3.0 * t)
        sig += 0.05 * np.sin(2 * np.pi * f * 4.2 * t)

        noise = np.random.uniform(-1, 1, samples) * 0.15 * np.exp(-t * 10)
        sig += noise

        env = np.exp(-t * 1.5)
        sig *= env

        return sig * note_event.note.velocity * 0.7


class Tambourine(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate

        noise = np.random.uniform(-1, 1, samples)
        hpf = HighPassFilter(cutoff=3000)
        noise = hpf.process(noise, self.sample_rate)

        env = np.exp(-t * 25)
        sig = noise * env

        jingle = 0.3 * np.sin(2 * np.pi * 8000 * t) * np.exp(-t * 30)
        sig += jingle

        return sig * note_event.note.velocity * 0.4


class Shaker(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        noise = np.random.uniform(-1, 1, samples)
        hpf = HighPassFilter(cutoff=5000)
        noise = hpf.process(noise, self.sample_rate)

        env = np.exp(-t * 40)
        return noise * env * note_event.note.velocity * 0.3


class Conga(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        pitch_env = 1.0 + 0.3 * np.exp(-t * 60)
        phase = 2 * np.pi * f * np.cumsum(pitch_env) / self.sample_rate
        body = np.sin(phase)

        noise = np.random.uniform(-1, 1, samples) * np.exp(-t * 20) * 0.3
        sig = body * np.exp(-t * 8) + noise

        return sig * note_event.note.velocity * 0.6


class Bongo(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        pitch_env = 1.0 + 0.4 * np.exp(-t * 80)
        phase = 2 * np.pi * f * np.cumsum(pitch_env) / self.sample_rate
        body = np.sin(phase)

        noise = np.random.uniform(-1, 1, samples) * np.exp(-t * 30) * 0.25
        sig = body * np.exp(-t * 12) + noise

        return sig * note_event.note.velocity * 0.5


class Tabla(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        pitch_env = 1.0 + 0.5 * np.exp(-t * 100)
        phase = 2 * np.pi * f * np.cumsum(pitch_env) / self.sample_rate
        body = np.sin(phase)

        harmonic = 0.3 * np.sin(2 * phase) * np.exp(-t * 15)
        noise = np.random.uniform(-1, 1, samples) * np.exp(-t * 25) * 0.15

        sig = (body + harmonic) * np.exp(-t * 5) + noise

        return sig * note_event.note.velocity * 0.6

import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, HighPassFilter


class Violin(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.15, decay=0.1, sustain=0.7, release=0.3)
        self.lpf = LowPassFilter(cutoff=5000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.008 * np.sin(2 * np.pi * 5.5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.6 * np.sin(phase)
        sig += 0.25 * np.sin(2 * phase)
        sig += 0.1 * np.sin(3 * phase)
        sig += 0.05 * np.sin(4 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.7


class Viola(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.18, decay=0.12, sustain=0.65, release=0.35)
        self.lpf = LowPassFilter(cutoff=4000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.007 * np.sin(2 * np.pi * 5.0 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.65 * np.sin(phase)
        sig += 0.2 * np.sin(2 * phase)
        sig += 0.1 * np.sin(3 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.65


class Cello(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.2, decay=0.15, sustain=0.6, release=0.4)
        self.lpf = LowPassFilter(cutoff=3500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.006 * np.sin(2 * np.pi * 4.5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.7 * np.sin(phase)
        sig += 0.2 * np.sin(2 * phase)
        sig += 0.07 * np.sin(3 * phase)
        sig += 0.03 * np.sin(4 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.75


class Contrabass(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.25, decay=0.2, sustain=0.5, release=0.5)
        self.lpf = LowPassFilter(cutoff=2000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.004 * np.sin(2 * np.pi * 3.5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.75 * np.sin(phase)
        sig += 0.15 * np.sin(2 * phase)
        sig += 0.07 * np.sin(3 * phase)
        sig += 0.03 * np.sin(5 * phase)

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.8


class Harp(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.997

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
        lpf = LowPassFilter(cutoff=3000)
        output = lpf.process(output, self.sample_rate)
        fade = min(500, samples)
        output[-fade:] *= np.linspace(1, 0, fade)

        return output * 0.6

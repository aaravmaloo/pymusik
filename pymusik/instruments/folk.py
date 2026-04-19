import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, BandPassFilter


class Banjo(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.97
        self.lpf = LowPassFilter(cutoff=4000)

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
        fade = min(150, samples)
        output[-fade:] *= np.linspace(1, 0, fade)

        return output * 0.6


class Mandolin(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.985
        self.lpf = LowPassFilter(cutoff=3500)

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

        sig = np.zeros(samples)
        for detune in [1.0, 1.002]:
            ring_buffer = np.random.uniform(-1, 1, L)
            output = np.zeros(samples)
            for i in range(samples):
                output[i] = ring_buffer[0]
                avg = 0.5 * (ring_buffer[0] + ring_buffer[1])
                new_sample = avg * self.damping
                ring_buffer = np.roll(ring_buffer, -1)
                ring_buffer[-1] = new_sample
            sig += output

        sig = sig / 2 * note_event.note.velocity
        sig = self.lpf.process(sig, self.sample_rate)
        fade = min(200, samples)
        sig[-fade:] *= np.linspace(1, 0, fade)

        return sig * 0.55


class Ukulele(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.99
        self.lpf = LowPassFilter(cutoff=2500)

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
        fade = min(250, samples)
        output[-fade:] *= np.linspace(1, 0, fade)

        return output * 0.5


class Sitar(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.damping = 0.993
        self.lpf = LowPassFilter(cutoff=2000)

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

        t = np.arange(samples) / self.sample_rate
        buzz = 0.15 * np.sin(2 * np.pi * freq * 5 * t) * np.exp(-t * 3)
        output += buzz

        output *= note_event.note.velocity
        output = self.lpf.process(output, self.sample_rate)
        fade = min(400, samples)
        output[-fade:] *= np.linspace(1, 0, fade)

        return output * 0.55


class Duduk(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.15, decay=0.1, sustain=0.7, release=0.2)
        self.bpf = BandPassFilter(low_cutoff=400, high_cutoff=3500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.012 * np.sin(2 * np.pi * 5.5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.6 * np.sin(phase)
        sig += 0.25 * np.sin(2 * phase)
        sig += 0.1 * np.sin(3 * phase)
        sig += 0.05 * np.sin(4 * phase)

        breath = np.random.uniform(-1, 1, samples) * 0.06
        sig += breath

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5


class Bagpipes(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.3, decay=0.1, sustain=0.85, release=0.3)
        self.lpf = LowPassFilter(cutoff=3000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.5 * np.sin(2 * np.pi * f * t)
        sig += 0.3 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.12 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.08 * np.sin(2 * np.pi * 5 * f * t)

        drone = 0.15 * np.sin(2 * np.pi * f * 0.5 * t)
        drone += 0.1 * np.sin(2 * np.pi * f * 1.0 * t)
        sig += drone

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5


class HurdyGurdy(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.2, decay=0.1, sustain=0.75, release=0.3)
        self.lpf = LowPassFilter(cutoff=2500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.55 * np.sin(2 * np.pi * f * t)
        sig += 0.25 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.12 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.08 * np.sin(2 * np.pi * 5 * f * t)

        drone = 0.1 * np.sin(2 * np.pi * f * 0.5 * t)
        sig += drone

        buzz = np.random.uniform(-1, 1, samples) * 0.03
        sig += buzz

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5

import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter


class PipeOrgan(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.05, decay=0.05, sustain=0.9, release=0.15)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = np.zeros(samples)
        harmonics = [1, 2, 3, 4, 6, 8, 10, 12, 16]
        amps = [1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05]
        for h, a in zip(harmonics, amps):
            sig += a * np.sin(2 * np.pi * f * h * t)

        sig /= sum(amps)
        sig = self.env.apply(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.6


class HammondOrgan(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.01, decay=0.01, sustain=0.9, release=0.05)
        self.lpf = LowPassFilter(cutoff=5000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        drawbars = [1.0, 0.8, 0.6, 0.0, 0.5, 0.0, 0.4, 0.3, 0.2]
        harmonics = [0.5, 1, 2, 3, 4, 6, 8, 10, 12]

        sig = np.zeros(samples)
        for d, h in zip(drawbars, harmonics):
            if d > 0:
                sig += d * np.sin(2 * np.pi * f * h * t)

        sig /= sum(d for d in drawbars if d > 0)

        rotary_lfo = 1.0 + 0.02 * np.sin(2 * np.pi * 6.8 * t)
        sig *= rotary_lfo

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.55


class Accordion(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.02, decay=0.05, sustain=0.8, release=0.1)
        self.lpf = LowPassFilter(cutoff=3500)

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

        tremolo = 1.0 + 0.15 * np.sin(2 * np.pi * 5.0 * t)
        sig *= tremolo

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.5


class Harmonium(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.03, decay=0.05, sustain=0.85, release=0.1)
        self.lpf = LowPassFilter(cutoff=2500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = 0.6 * np.sin(2 * np.pi * f * t)
        sig += 0.25 * np.sin(2 * np.pi * 2 * f * t)
        sig += 0.1 * np.sin(2 * np.pi * 3 * f * t)
        sig += 0.05 * np.sin(2 * np.pi * 5 * f * t)

        drone = 0.08 * np.sin(2 * np.pi * f * 0.5 * t)
        sig += drone

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.lpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.55

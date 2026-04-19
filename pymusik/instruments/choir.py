import numpy as np
from .base import Instrument
from ..core.time import TimeContext
from ..core.events import NoteEvent
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter, BandPassFilter


class ChoirPad(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.6, decay=0.4, sustain=0.7, release=0.8)
        self.bpf = BandPassFilter(low_cutoff=300, high_cutoff=4000)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        sig = np.zeros(samples)
        for d in [1.0, 1.003, 0.997, 1.006, 0.994]:
            phase = 2 * np.pi * f * d * t
            sig += 0.5 * np.sin(phase)
            sig += 0.3 * np.sin(2 * phase)
            sig += 0.2 * np.sin(3 * phase)

        sig /= 5

        noise = np.random.uniform(-1, 1, samples) * 0.04
        sig += noise

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.4


class VocalOoh(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.3, decay=0.2, sustain=0.7, release=0.4)
        self.bpf = BandPassFilter(low_cutoff=400, high_cutoff=3200)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.006 * np.sin(2 * np.pi * 5.5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.7 * np.sin(phase)
        sig += 0.2 * np.sin(2 * phase)
        sig += 0.07 * np.sin(3 * phase)
        sig += 0.03 * np.sin(4 * phase)

        formant1 = 0.3 * np.sin(2 * np.pi * 300 * t)
        formant2 = 0.15 * np.sin(2 * np.pi * 870 * t)
        sig += formant1 + formant2

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.4


class VocalAah(Instrument):
    def __init__(self, sample_rate: int = 44100):
        super().__init__(sample_rate)
        self.env = ADSREnvelope(attack=0.25, decay=0.15, sustain=0.7, release=0.35)
        self.bpf = BandPassFilter(low_cutoff=400, high_cutoff=4500)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        samples = time_context.beats_to_samples(note_event.note.duration)
        if samples <= 0:
            return np.array([])

        t = np.arange(samples) / self.sample_rate
        f = note_event.note.pitch.frequency

        vibrato = 1.0 + 0.007 * np.sin(2 * np.pi * 5.5 * t)
        phase = 2 * np.pi * f * np.cumsum(vibrato) / self.sample_rate

        sig = 0.6 * np.sin(phase)
        sig += 0.25 * np.sin(2 * phase)
        sig += 0.1 * np.sin(3 * phase)
        sig += 0.05 * np.sin(4 * phase)

        formant1 = 0.25 * np.sin(2 * np.pi * 730 * t)
        formant2 = 0.15 * np.sin(2 * np.pi * 1090 * t)
        formant3 = 0.08 * np.sin(2 * np.pi * 2440 * t)
        sig += formant1 + formant2 + formant3

        breath = np.random.uniform(-1, 1, samples) * 0.03
        sig += breath

        sig = self.env.apply(sig, self.sample_rate)
        sig = self.bpf.process(sig, self.sample_rate)
        return sig * note_event.note.velocity * 0.4

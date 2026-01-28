import numpy as np
from .base import Instrument
from ..synthesis.oscillators import SineOscillator, SawtoothOscillator, SquareOscillator
from ..synthesis.envelopes import ADSREnvelope
from ..synthesis.filters import LowPassFilter
from ..core.time import TimeContext
from ..core.events import NoteEvent

class SynthInstrument(Instrument):
    def __init__(self, sample_rate: int = 44100, oscillator_type: str = "saw"):
        super().__init__(sample_rate)
        
        if oscillator_type == "sine":
            self.osc = SineOscillator(sample_rate)
        elif oscillator_type == "square":
            self.osc = SquareOscillator(sample_rate)
        else:
            self.osc = SawtoothOscillator(sample_rate)
            
        self.envelope = ADSREnvelope(attack=0.01, decay=0.1, sustain=0.7, release=0.1)
        self.filter = LowPassFilter(cutoff=2000.0)

    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        duration_samples = time_context.beats_to_samples(note_event.note.duration)
        if duration_samples <= 0:
            return np.array([])
            
        freq = note_event.note.pitch.frequency
        signal = self.osc.generate(freq, duration_samples)
        signal = self.envelope.apply(signal, self.sample_rate)
        signal = self.filter.process(signal, self.sample_rate)
        signal *= note_event.note.velocity
        
        return signal

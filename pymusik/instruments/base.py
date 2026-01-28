from abc import ABC, abstractmethod
import numpy as np
from ..core.time import TimeContext
from ..core.events import NoteEvent

class Instrument(ABC):
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    @abstractmethod
    def process_note(self, note_event: NoteEvent, time_context: TimeContext) -> np.ndarray:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(sr={self.sample_rate})"

from typing import List, Union, Optional
from ..core.pitch import Note, Pitch, Rest

class Pattern:
    def __init__(self, elements: List[Union[Note, str, Pitch, None]] = None, loop: bool = False, length_beats: Optional[float] = None):
        self.elements = []
        self.loop = loop
        self._explicit_length = length_beats
        if elements:
            for el in elements:
                if isinstance(el, (Note, Pitch, Rest)):
                    self.elements.append(el)
                elif isinstance(el, str):
                    self.elements.append(Note(el))
                elif el is None:
                    self.elements.append(Rest(1.0))
                else:
                    self.elements.append(el)
                    
    @property
    def duration(self) -> float:
        if self._explicit_length is not None:
            return self._explicit_length
        return sum(el.duration for el in self.elements if hasattr(el, 'duration'))

    def add_note(self, pitch: Union[str, Pitch], duration: float = 1.0, velocity: float = 0.8):
        self.elements.append(Note(pitch, duration, velocity))

    def add_rest(self, duration: float = 1.0):
        self.elements.append(Rest(duration))

    def humanize(self, velocity_jitter: float = 0.1):
        import random
        for el in self.elements:
            if isinstance(el, Note):
                jitter = (random.random() * 2 - 1) * velocity_jitter
                el.velocity = max(0.1, min(1.0, el.velocity + jitter))
        return self

    def __repr__(self):
        return f"Pattern(len={len(self.elements)})"

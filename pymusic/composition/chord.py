from typing import List, Union
from ..core.pitch import Pitch, Note

class Chord:
    CHORD_TYPES = {
        "major": [0, 4, 7],
        "minor": [0, 3, 7],
        "diminished": [0, 3, 6],
        "augmented": [0, 4, 8],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dom7": [0, 4, 7, 10],
    }

    def __init__(self, root: str, chord_type: str = "major", octave: int = 4):
        self.root_name = root.capitalize()
        self.chord_type = chord_type
        self.octave = octave
        self.intervals = self.CHORD_TYPES.get(chord_type, self.CHORD_TYPES["major"])

    def get_pitches(self) -> List[Pitch]:
        root_pitch = Pitch(f"{self.root_name}{self.octave}")
        return [root_pitch.transpose(i) for i in self.intervals]

    def to_notes(self, duration: float = 1.0, velocity: float = 0.8) -> List[Note]:
        return [Note(p, duration, velocity) for p in self.get_pitches()]

    def __repr__(self):
        return f"Chord({self.root_name}, {self.chord_type})"

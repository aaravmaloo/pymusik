import re
from typing import Union, List, Optional
from .constants import A4_FREQ, NOTE_NAMES, FLAT_NAMES, SCALES

class Pitch:
    def __init__(self, name_or_midi: Union[str, int]):
        if isinstance(name_or_midi, int):
            self.midi = name_or_midi
        else:
            self.midi = self._parse_note_name(name_or_midi)
            
    @property
    def frequency(self) -> float:
        return A4_FREQ * (2 ** ((self.midi - 69) / 12))
    
    @property
    def name(self) -> str:
        octave = (self.midi // 12) - 1
        name = NOTE_NAMES[self.midi % 12]
        return f"{name}{octave}"

    def _parse_note_name(self, name: str) -> int:
        match = re.match(r"([A-Ga-g][#b]?)(-?\d+)", name)
        if not match:
            raise ValueError(f"Invalid note name: {name}")
        
        note_part = match.group(1).capitalize()
        octave_part = int(match.group(2))
        
        if note_part in NOTE_NAMES:
            index = NOTE_NAMES.index(note_part)
        elif note_part in FLAT_NAMES:
            index = FLAT_NAMES.index(note_part)
        else:
            raise ValueError(f"Invalid note: {note_part}")
            
        return (octave_part + 1) * 12 + index

    def transpose(self, semitones: int) -> 'Pitch':
        return Pitch(self.midi + semitones)

    def __repr__(self):
        return f"Pitch({self.name})"

class Note:
    def __init__(self, pitch: Union[str, int, Pitch], duration: float = 1.0, velocity: float = 0.8):
        self.pitch = pitch if isinstance(pitch, Pitch) else Pitch(pitch)
        self.duration = duration
        self.velocity = velocity
        
    def __repr__(self):
        return f"Note({self.pitch.name}, dur={self.duration}, vel={self.velocity})"

class Rest:
    def __init__(self, duration: float = 1.0):
        self.duration = duration
        
    def __repr__(self):
        return f"Rest(dur={self.duration})"

class Scale:
    def __init__(self, root: str, scale_type: str = "major"):
        self.root_name = root.capitalize()
        self.intervals = SCALES.get(scale_type, SCALES["major"])
        self.scale_type = scale_type

    def get_notes(self, octave: int = 4) -> List[Pitch]:
        root_pitch = Pitch(f"{self.root_name}{octave}")
        return [root_pitch.transpose(i) for i in self.intervals]

    def __repr__(self):
        return f"Scale({self.root_name}, {self.scale_type})"

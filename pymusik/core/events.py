from dataclasses import dataclass
from typing import Optional, Any
from .pitch import Note

@dataclass
class Event:
    time: float

@dataclass
class NoteEvent(Event):
    note: Note
    
    @property
    def duration(self) -> float:
        return self.note.duration

@dataclass
class ParameterEvent(Event):
    parameter: str
    value: Any
    target_id: Optional[str] = None

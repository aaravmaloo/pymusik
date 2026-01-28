from typing import List, Dict, Optional
import numpy as np
from ..instruments.base import Instrument
from ..composition.pattern import Pattern
from ..core.time import TimeContext
from ..core.events import NoteEvent, Event
from ..core.pitch import Note, Rest

class Track:
    def __init__(self, name: str, instrument: Instrument):
        self.name = name
        self.instrument = instrument
        self.pattern: Optional[Pattern] = None
        self.gain: float = 0.8
        self.sidechain: bool = False
        
    def set_pattern(self, pattern: Pattern):
        self.pattern = pattern

    def get_events(self, total_beats: Optional[float] = None) -> List[NoteEvent]:
        events = []
        if not self.pattern or not self.pattern.elements:
            return events
            
        current_time = 0.0
        pattern_duration = self.pattern.duration
        
        while True:
            for el in self.pattern.elements:
                event_time = current_time
                if isinstance(el, Note):
                    events.append(NoteEvent(time=event_time, note=el))
                    current_time += el.duration
                elif isinstance(el, Rest):
                    current_time += el.duration
                
                if total_beats is not None and current_time >= total_beats:
                    return events
            
            if not self.pattern.loop:
                break
            
            if pattern_duration <= 0:
                break
                
            if total_beats is None:
                break
                
        return events

class Song:
    def __init__(self, name: str = "Untitled", bpm: float = 120.0, sample_rate: int = 44100, duration_beats: Optional[float] = None):
        self.name = name
        self.time_context = TimeContext(bpm=bpm, sample_rate=sample_rate)
        self.tracks: List[Track] = []
        self.duration_beats = duration_beats

    def create_track(self, name: str, instrument: Instrument) -> Track:
        track = Track(name, instrument)
        self.tracks.append(track)
        return track

    def get_total_duration_beats(self) -> float:
        if self.duration_beats is not None:
            return self.duration_beats
            
        max_duration = 0.0
        for track in self.tracks:
            events = track.get_events()
            if events:
                last_event = events[-1]
                max_duration = max(max_duration, last_event.time + last_event.duration)
        return max_duration

    def render(self, filename: str, sample_rate: Optional[int] = None):
        from .renderer import Renderer
        from ..output.audio import save_wav
        
        if sample_rate:
            self.time_context.sample_rate = sample_rate
            
        renderer = Renderer(self)
        audio_data = renderer.render()
        save_wav(filename, audio_data, self.time_context.sample_rate)

    def export_midi(self, filename: str):
        from ..output.midi import export_midi
        export_midi(self, filename)

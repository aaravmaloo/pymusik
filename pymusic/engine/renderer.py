import numpy as np
from .audio_graph import Song

class Renderer:
    def __init__(self, song: Song):
        self.song = song

    def render(self) -> np.ndarray:
        total_beats = self.song.get_total_duration_beats()
        total_samples = self.song.time_context.beats_to_samples(total_beats)
        
        padding_samples = self.song.time_context.sample_rate * 1
        master_buffer = np.zeros(total_samples + padding_samples)
        
        for track in self.song.tracks:
            events = track.get_events(total_beats=total_beats)
            for event in events:
                start_sample = self.song.time_context.beats_to_samples(event.time)
                note_signal = track.instrument.process_note(event, self.song.time_context)
                
                if len(note_signal) == 0:
                    continue
                
                end_sample = start_sample + len(note_signal)
                if end_sample > len(master_buffer):
                    new_size = end_sample + self.song.time_context.sample_rate
                    new_buffer = np.zeros(new_size)
                    new_buffer[:len(master_buffer)] = master_buffer
                    master_buffer = new_buffer
                    
                master_buffer[start_sample:end_sample] += note_signal * track.gain
                
        max_val = np.max(np.abs(master_buffer))
        if max_val > 1.0:
            master_buffer /= max_val
            
        return master_buffer

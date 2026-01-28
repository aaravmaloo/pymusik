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
        
        # Ducking Envelope for Sidechain (Techno Pumping)
        duck_size = len(master_buffer)
        t_duck = np.arange(duck_size) / self.song.time_context.sample_rate
        beat_pos = (t_duck * (self.song.time_context.bpm / 60.0)) % 1.0
        duck_env = 1.0 - 0.8 * np.exp(-4.0 * beat_pos)

        for track in self.song.tracks:
            track_buffer = np.zeros(len(master_buffer))
            events = track.get_events(total_beats=total_beats)
            for event in events:
                start_sample = self.song.time_context.beats_to_samples(event.time)
                note_signal = track.instrument.process_note(event, self.song.time_context)
                
                if len(note_signal) == 0: continue
                
                end_sample = start_sample + len(note_signal)
                if end_sample > len(track_buffer):
                    track_buffer = np.pad(track_buffer, (0, end_sample - len(track_buffer)))
                    if len(track_buffer) > len(master_buffer):
                        master_buffer = np.pad(master_buffer, (0, len(track_buffer) - len(master_buffer)))
                        duck_env = np.pad(duck_env, (0, len(track_buffer) - len(duck_env)), constant_values=1.0)

                track_buffer[start_sample:end_sample] += note_signal * track.gain
            
            if track.sidechain:
                track_buffer *= duck_env[:len(track_buffer)]
            
            master_buffer[:len(track_buffer)] += track_buffer
                
        # Master Limiter / Soft Saturation
        master_buffer = np.tanh(master_buffer * 1.2) # Saturate for warmth
        max_val = np.max(np.abs(master_buffer))
        if max_val > 0.98:
            master_buffer /= (max_val / 0.98)
            
        return master_buffer

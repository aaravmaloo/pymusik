import mido
from mido import Message, MidiFile, MidiTrack
from ..engine.audio_graph import Song

def export_midi(song: Song, filename: str):
    mid = MidiFile()
    mid.ticks_per_beat = 480
    
    for track_obj in song.tracks:
        midi_track = MidiTrack()
        mid.tracks.append(midi_track)
        midi_track.append(mido.MetaMessage('track_name', name=track_obj.name))
        
        events = track_obj.get_events()
        last_tick = 0
        
        for event in events:
            start_tick = int(event.time * mid.ticks_per_beat)
            delta_tick = start_tick - last_tick
            
            midi_track.append(Message('note_on', note=event.note.pitch.midi, 
                                     velocity=int(event.note.velocity * 127), 
                                     time=delta_tick))
            
            duration_ticks = int(event.note.duration * mid.ticks_per_beat)
            midi_track.append(Message('note_off', note=event.note.pitch.midi, 
                                      velocity=0, 
                                      time=duration_ticks))
            
            last_tick = start_tick + duration_ticks

    mid.save(filename)

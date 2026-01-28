from pymusic.core.pitch import Note, Scale, Pitch
from pymusic.composition.pattern import Pattern
from pymusic.instruments.phonk import PhonkCowbell, Bass808
from pymusic.instruments.drums import DrumInstrument
from pymusic.engine.audio_graph import Song

def create_phonk():
    print("Generating PHONK... (Memphis intensity rising)")
    
    # 1. Setup Song
    total_beats = 128 # 1 minute approx
    song = Song(name="Code Phonk", bpm=125, duration_beats=total_beats)
    
    # 2. Heavy 808 Bass
    bass808 = Bass808()
    bass_track = song.create_track("808", bass808)
    bass_track.gain = 1.0
    
    bass_pat = Pattern(loop=True, length_beats=16.0)
    # Simple aggressive 808 pattern
    bass_pat.add_note("C2", duration=2.0)
    bass_pat.add_note("C2", duration=2.0)
    bass_pat.add_note("D#2", duration=2.0)
    bass_pat.add_note("F2", duration=2.0)
    bass_track.set_pattern(bass_pat)
    
    # 3. The Iconic PHONK COWBELL
    cowbell = PhonkCowbell()
    bell_track = song.create_track("Cowbell", cowbell)
    bell_track.gain = 0.6
    
    # Typical dark, repetitive cowbell melody
    bell_pat = Pattern(loop=True, length_beats=16.0)
    melody = ["C5", "C5", "D#5", "C5", "F5", "C5", "D#5", "D5"]
    for m in melody:
        bell_pat.add_note(m, duration=0.5, velocity=0.9)
        bell_pat.add_rest(0.5)
    bell_track.set_pattern(bell_pat)
    
    # 4. Drums: Drift Style
    drum_inst = DrumInstrument()
    drums = song.create_track("Drums", drum_inst)
    
    drum_pat = Pattern(loop=True, length_beats=4.0)
    drum_pat.add_note("C1", duration=1.0) # Thick Kick
    drum_pat.add_note("D1", duration=1.0) # Sharp Snare
    drum_pat.add_note("C1", duration=0.75)
    drum_pat.add_note("C1", duration=0.25)
    drum_pat.add_note("D1", duration=1.0)
    drums.set_pattern(drum_pat)
    
    # 5. Render
    print("Rendering phonk_drift.wav...")
    song.render("phonk_drift.wav")
    print("Exporting MIDI...")
    song.export_midi("phonk_drift.mid")
    

if __name__ == "__main__":
    create_phonk()

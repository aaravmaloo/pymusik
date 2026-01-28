from pymusik.core.pitch import Note, Scale, Pitch
from pymusik.composition.pattern import Pattern
from pymusik.instruments.phonk import PhonkCowbell, Bass808
from pymusik.instruments.drums import DrumInstrument
from pymusik.engine.audio_graph import Song

def create_phonk():
    print("Generating HEAVY PHONK... (Feel the Bass)")
    
    # 1. Setup Song
    total_beats = 64 # 30 seconds of intensity
    song = Song(name="Heavy Phonk", bpm=130, duration_beats=total_beats)
    
    # 2. ULTRA HEAVY 808
    bass808 = Bass808()
    bass_track = song.create_track("808", bass808)
    bass_track.gain = 1.5 # CRANK IT
    
    # 4-bar heavy 808 pattern
    bass_pat = Pattern(loop=True, length_beats=16.0)
    # Long notes to let the 808 develop
    bass_pat.add_note("C2", duration=2.0, velocity=1.0)
    bass_pat.add_note("C2", duration=1.0, velocity=0.8)
    bass_pat.add_note("F1", duration=1.0, velocity=0.9) # Lower root for more sub
    bass_pat.add_note("C2", duration=2.0, velocity=1.0)
    bass_pat.add_note("G#1", duration=1.0, velocity=0.9)
    bass_pat.add_note("G1", duration=1.0, velocity=0.8)
    bass_track.set_pattern(bass_pat)
    
    # 3. Cowbell Melody
    cowbell = PhonkCowbell()
    bell_track = song.create_track("Cowbell", cowbell)
    bell_track.gain = 0.5
    
    bell_pat = Pattern(loop=True, length_beats=8.0)
    # Dark Phonk melody (Minor scale)
    melody = ["C5", "C5", "C5", "D#5", "F5", "D#5", "C5", "A#4"]
    for m in melody:
        bell_pat.add_note(m, duration=0.25, velocity=0.8)
        bell_pat.add_rest(0.75)
    bell_track.set_pattern(bell_pat)
    
    # 4. Drums (Hard Trap Kits)
    drum_inst = DrumInstrument()
    drums = song.create_track("Drums", drum_inst)
    
    drum_pat = Pattern(loop=True, length_beats=4.0)
    drum_pat.add_note("C1", duration=0.5)  # Hard Kick
    drum_pat.add_rest(0.5)
    drum_pat.add_note("D1", duration=1.0)  # Snare
    drum_pat.add_note("C1", duration=0.25) # Fast kick double
    drum_pat.add_note("C1", duration=0.75)
    drum_pat.add_note("D1", duration=1.0)
    drums.set_pattern(drum_pat)
    
    # 5. Render
    print("Rendering heavy_phonk.wav...")
    song.render("heavy_phonk.wav")

if __name__ == "__main__":
    create_phonk()

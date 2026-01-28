import numpy as np
from pymusic.core.pitch import Note, Scale, Pitch
from pymusic.composition.pattern import Pattern
from pymusic.instruments.synth import SynthInstrument
from pymusic.instruments.piano import PianoInstrument
from pymusic.instruments.drums import DrumInstrument
from pymusic.instruments.phonk import PhonkCowbell, Bass808
from pymusic.instruments.lofi import GuitarInstrument, SaxInstrument, MellowPiano, VinylEffect
from pymusic.engine.audio_graph import Song

def create_ultimate_layered_song():
    print("Starting the Ultimate LAYERED Musical Journey...")
    
    # 2 Minutes at 120 BPM = 240 Beats
    total_beats = 240
    song = Song(name="Pymusic Multi-Layer Odyssey", bpm=120, duration_beats=total_beats)
    
    # --- INSTRUMENT SETUP ---
    vinyl = song.create_track("Vinyl", VinylEffect())
    vinyl.gain = 0.12
    
    drums = song.create_track("Drums", DrumInstrument())
    drums.gain = 0.75
    
    rhodes = song.create_track("Rhodes", MellowPiano())
    rhodes.gain = 0.45
    
    bass = song.create_track("Bass808", Bass808())
    bass.gain = 0.85
    
    guitar = song.create_track("Guitar", GuitarInstrument())
    guitar.gain = 0.35
    
    cowbell = song.create_track("PhonkBell", PhonkCowbell())
    cowbell.gain = 0.4
    
    sax = song.create_track("Sax", SaxInstrument())
    sax.gain = 0.35

    # --- SIMULTANEOUS LAYERING ---

    # 1. Background Atmosphere (Vinyl) - Plays throughout
    v_pat = Pattern(loop=True, length_beats=16.0)
    v_pat.add_note("C4", duration=16.0)
    vinyl.set_pattern(v_pat)

    # 2. Continuous Drums (Phonk-inspired rhythm) - Plays throughout
    d_pat = Pattern(loop=True, length_beats=4.0)
    d_pat.add_note("C1", duration=1.0, velocity=0.9) # Kick
    d_pat.add_note("F1", duration=0.5, velocity=0.4) # Hat
    d_pat.add_note("D1", duration=0.5, velocity=1.0) # Snare
    d_pat.add_note("C1", duration=0.5, velocity=0.7) # Ghost Kick
    d_pat.add_note("F1", duration=0.5, velocity=0.5) # Hat
    d_pat.add_note("D1", duration=1.0, velocity=1.0) # Snare
    drums.set_pattern(d_pat)

    # 3. Rhodes Chord Progression (Jazzy) - Plays throughout
    r_pat = Pattern(loop=True, length_beats=16.0)
    progressions = [("D3", 4.0), ("G2", 4.0), ("C3", 8.0)]
    for note, dur in progressions:
        r_pat.add_note(note, duration=dur, velocity=0.5)
    rhodes.set_pattern(r_pat)

    # 4. Bass Line (Subby 808) - Joins at beat 32
    # We use a pattern that starts with rests for 32 beats
    b_pat = Pattern(loop=False, length_beats=total_beats)
    b_pat.add_rest(32.0)
    # Loop manually or add repeating notes
    for _ in range(26): # (240-32)/8 = 26ish
        b_pat.add_note("C2", duration=4.0, velocity=1.0)
        b_pat.add_note("F1", duration=4.0, velocity=0.9)
    bass.set_pattern(b_pat)

    # 5. Guitar Melody - Joins at beat 64
    g_pat = Pattern(loop=False, length_beats=total_beats)
    g_pat.add_rest(64.0)
    g_melody = [("E4", 2.0), ("G4", 2.0), ("A4", 4.0), ("B4", 4.0), ("C5", 4.0)]
    for _ in range(11):
        for n, d in g_melody:
            g_pat.add_note(n, duration=d, velocity=0.4)
    guitar.set_pattern(g_pat)

    # 6. Phonk Cowbell Lead - Joins at beat 96
    c_pat = Pattern(loop=False, length_beats=total_beats)
    c_pat.add_rest(96.0)
    c_melody = [("C5", 0.5), ("C5", 0.5), ("E5", 1.0), ("D5", 1.0), ("C5", 1.0)]
    for _ in range(18):
        for n, d in c_melody:
            c_pat.add_note(n, duration=d, velocity=0.7)
        c_pat.add_rest(4.0)
    cowbell.set_pattern(c_pat)

    # 7. Saxophone Soul - Joins at beat 144
    s_pat = Pattern(loop=False, length_beats=total_beats)
    s_pat.add_rest(144.0)
    s_melody = [("G4", 4.0), ("A4", 4.0), ("C5", 8.0)]
    for _ in range(6):
        for n, d in s_melody:
            s_pat.add_note(n, duration=d, velocity=0.6)
    sax.set_pattern(s_pat)

 
    song.render("ultimate_odyssey.wav")
  

if __name__ == "__main__":
    create_ultimate_layered_song()

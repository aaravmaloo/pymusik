from pymusic.core.pitch import Note, Scale, Pitch
from pymusic.composition.pattern import Pattern
from pymusic.instruments.lofi import GuitarInstrument, SaxInstrument, MellowPiano, VinylEffect
from pymusic.instruments.drums import DrumInstrument
from pymusic.engine.audio_graph import Song

def create_lofi():
    print("Creating Lo-Fi chill vibes...")
    
    # 1. Setup Song (Lo-fi is slow: 80-90 BPM)
    total_beats = 64
    song = Song(name="Chill Code", bpm=85, duration_beats=total_beats)
    
    # 2. Vinyl Crackle (Background Atmosphere)
    v_inst = VinylEffect()
    v_track = song.create_track("Vinyl", v_inst)
    v_track.gain = 0.3
    v_pat = Pattern(loop=True, length_beats=16.0)
    v_pat.add_note("C4", duration=16.0) # Just to trigger the effect
    v_track.set_pattern(v_pat)
    
    # 3. Mellow Rhodes/Piano (Chords)
    piano = MellowPiano()
    p_track = song.create_track("Rhodes", piano)
    p_track.gain = 0.6
    
    p_pat = Pattern(loop=True, length_beats=16.0)
    # Jazzy II-V-I progression in C Major
    # Dm7 - G7 - Cmaj7 - Cmaj7
    chords = [
        (["D3", "F3", "A3", "C4"], 4.0),
        (["G2", "B3", "D4", "F4"], 4.0),
        (["C3", "E3", "G3", "B3"], 8.0)
    ]
    for notes, dur in chords:
        for n in notes:
            p_pat.add_note(n, duration=dur, velocity=0.6)

        pass
    
    # Better approach for chords in current Pattern:
    p_pat = Pattern(loop=True, length_beats=16.0)
   
    p_pat.add_note("D3", duration=4.0)
    p_pat.add_note("G2", duration=4.0)
    p_pat.add_note("C3", duration=8.0)
    p_track.set_pattern(p_pat)
    
    # 4. Lo-Fi Guitar (Melody)
    guitar = GuitarInstrument()
    g_track = song.create_track("Guitar", guitar)
    g_track.gain = 0.4
    
    g_pat = Pattern(loop=True, length_beats=8.0)
    g_melody = [("E4", 1.0), ("G4", 1.0), ("A4", 2.0), ("G4", 4.0)]
    for n, d in g_melody:
        g_pat.add_note(n, duration=d, velocity=0.5)
    g_track.set_pattern(g_pat)
    
    # 5. Smooth Sax (Soulful licks)
    sax = SaxInstrument()
    s_track = song.create_track("Sax", sax)
    s_track.gain = 0.3
    
    s_pat = Pattern(loop=True, length_beats=32.0)
    s_pat.add_rest(16.0) # Wait for half the cycle
    s_pat.add_note("C5", duration=2.0)
    s_pat.add_note("B4", duration=2.0)
    s_pat.add_note("A4", duration=4.0)
    s_track.set_pattern(s_pat)
    
    # 6. Lo-Fi Drums (Boombap feel)
    drums = song.create_track("Drums", DrumInstrument())
    drums.gain = 0.7
    
    d_pat = Pattern(loop=True, length_beats=4.0)
    d_pat.add_note("C1", duration=1.0) # Kick
    d_pat.add_note("F1", duration=1.0) # Hat
    d_pat.add_note("D1", duration=0.5) # Snare
    d_pat.add_note("F1", duration=0.5) # Hat
    d_pat.add_note("C1", duration=0.5) # Kick
    d_pat.add_note("D1", duration=0.5) # Snare
    drums.set_pattern(d_pat)
    
    # Render
    
    song.render("lofi_chill.wav")
    

if __name__ == "__main__":
    create_lofi()

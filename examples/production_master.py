from pymusik.core.pitch import Note, Scale, Pitch
from pymusik.composition.pattern import Pattern
from pymusik.composition.chord import Chord
from pymusik.instruments.pro import ProDrums, AnalogLead, AtmosphericStrings, AcidBass
from pymusik.instruments.lofi import VinylEffect, MellowPiano
from pymusik.engine.audio_graph import Song

def create_real_production():
    print("💎 Composing 'Ethereal Systems' - A High-Fidelity Master Production...")
    
    # 2-minute cinematic journey at 124 BPM
    total_beats = 248
    song = Song(name="Ethereal Systems", bpm=124, duration_beats=total_beats)
    
    # --- INSTRUMENTS & TRACKS ---
    
    # Textural Foundation
    v_track = song.create_track("Vinyl", VinylEffect())
    v_track.gain = 0.12
    
    strings = song.create_track("Strings", AtmosphericStrings())
    strings.gain = 0.35
    
    rhodes = song.create_track("Rhodes", MellowPiano())
    rhodes.gain = 0.4
    
    # The Beat
    drums = song.create_track("Drums", ProDrums())
    drums.gain = 0.85
    
    # The Energy (Sidechained)
    bass = song.create_track("AcidBass", AcidBass())
    bass.gain = 0.7
    bass.sidechain = True 
    
    lead = song.create_track("AnalogLead", AnalogLead())
    lead.gain = 0.5
    lead.sidechain = True

    # --- COMPOSITION WITH HUMANIZATION ---

    # 1. Background Atmosphere
    v_pat = Pattern(loop=True, length_beats=16.0)
    v_pat.add_note("C4", duration=16.0)
    v_track.set_pattern(v_pat)

    # 2. Cinematic Strings (Humanized)
    s_pat = Pattern(loop=True, length_beats=32.0)
    s_chords = ["C3", "G#2", "A#2", "F2"]
    for c in s_chords:
        s_pat.add_note(c, duration=8.0, velocity=0.5)
    s_pat.humanize(velocity_jitter=0.15) # Add organic volume drift
    strings.set_pattern(s_pat)

    # 3. Jazzy Rhodes (Humanized)
    r_pat = Pattern(loop=True, length_beats=16.0)
    r_notes = [("C3", 2.0), ("E3", 2.0), ("G3", 4.0), ("F3", 8.0)]
    for n, d in r_notes:
        r_pat.add_note(n, duration=d, velocity=0.4)
    r_pat.humanize(velocity_jitter=0.2) # Make it feel played by hand
    rhodes.set_pattern(r_pat)

    # 4. Driving Drums
    d_pat = Pattern(loop=True, length_beats=4.0)
    d_pat.add_note("C1", duration=1.0, velocity=1.0) # Kick
    d_pat.add_note("F1", duration=0.5, velocity=0.4) # Hat
    d_pat.add_note("D1", duration=0.5, velocity=0.9) # Snare
    d_pat.add_note("C1", duration=0.5, velocity=0.7)
    d_pat.add_note("F1", duration=0.5, velocity=0.5)
    d_pat.add_note("D1", duration=1.0, velocity=1.0)
    drums.set_pattern(d_pat)

    # 5. Evolving Acid Bass
    b_pat = Pattern(loop=True, length_beats=8.0)
    b_pat.add_note("C2", duration=2.0, velocity=0.8)
    b_pat.add_note("C2", duration=2.0, velocity=0.6)
    b_pat.add_note("G#1", duration=4.0, velocity=0.7)
    bass.set_pattern(b_pat)

    # 6. Emotional Analog Lead (Enters at beat 64)
    l_pat = Pattern(loop=False, length_beats=total_beats)
    l_pat.add_rest(64.0)
    l_melody = [("C4", 1.0), ("G4", 1.0), ("A#4", 2.0), ("F4", 4.0)]
    for _ in range(23): # Repeat until end
        for n, d in l_melody:
            l_pat.add_note(n, duration=d, velocity=0.6)
    l_pat.humanize(velocity_jitter=0.2)
    lead.set_pattern(l_pat)

    # --- RENDER ---
    print(f"🔊 Rendering 'Ethereal Systems' ({total_beats} beats)...")
    # Master saturation/limiting is applied inside renderer
    song.render("ethereal_systems.wav")
    print("💎 Production Complete. This is real music. 🌌🎶✨")

if __name__ == "__main__":
    create_real_production()

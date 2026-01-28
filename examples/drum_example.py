from pymusic.core.pitch import Note
from pymusic.composition.pattern import Pattern
from pymusic.instruments.drums import DrumInstrument
from pymusic.engine.audio_graph import Song

def create_drums():
    
    # 1. Setup Song
    total_beats = 32
    song = Song(name="Drum Showcase", bpm=120, duration_beats=total_beats)
    
    # 2. Basic Rock/Pop Beat
    rock_inst = DrumInstrument()
    rock_track = song.create_track("Rock_Drums", rock_inst)
    
    rock_pat = Pattern(loop=True, length_beats=4.0)
    # Beat 1: Kick
    rock_pat.add_note("C1", duration=1.0)
    # Beat 2: Snare + Hat
    rock_pat.add_note("D1", duration=0.5)
    rock_pat.add_note("F1", duration=0.5)
    # Beat 3: Kick
    rock_pat.add_note("C1", duration=1.0)
    # Beat 4: Snare + Hat
    rock_pat.add_note("D1", duration=0.5)
    rock_pat.add_note("F1", duration=0.5)
    
    rock_track.set_pattern(rock_pat)
    
    # 3. Fast Trap-style Hats (Adding another track for complexity)
    trap_hats = song.create_track("Trap_Hats", rock_inst)
    trap_pat = Pattern(loop=True, length_beats=4.0)
    
    # Rolling 1/8th and 1/16th notes
    for i in range(8):
        trap_pat.add_note("F1", duration=0.25, velocity=0.6)
        trap_pat.add_note("F1", duration=0.25, velocity=0.4)
    
    trap_hats.set_pattern(trap_pat)
    trap_hats.gain = 0.5
    
    # Render
    print("Rendering drum_showcase.wav...")
    song.render("drum_showcase.wav")

if __name__ == "__main__":
    create_drums()

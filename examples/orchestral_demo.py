from pymusik.core.pitch import Note, Scale
from pymusik.composition.pattern import Pattern
from pymusik.instruments.strings import Violin, Viola, Cello, Contrabass, Harp
from pymusik.instruments.brass import Trumpet, FrenchHorn
from pymusik.instruments.woodwinds import Flute, Oboe, Bassoon
from pymusik.instruments.percussion import Timpani, Gong
from pymusik.engine.audio_graph import Song


def main():
    print("=== Orchestral Demo ===")

    song = Song(name="Symphonic Sketch", bpm=72)

    # Strings section
    violin = song.create_track("Violin", Violin())
    violin.set_pattern(Pattern(["C5", "E5", "G5", "B4"], loop=True, length_beats=8.0))
    violin.gain = 0.6

    viola = song.create_track("Viola", Viola())
    viola.set_pattern(Pattern(["G4", "C4", "E4", "G3"], loop=True, length_beats=8.0))
    viola.gain = 0.5

    cello = song.create_track("Cello", Cello())
    cello.set_pattern(Pattern(["C3", "G2", "A2", "F2"], loop=True, length_beats=8.0))
    cello.gain = 0.6

    bass = song.create_track("Contrabass", Contrabass())
    bass.set_pattern(Pattern(["C2", None, "G1", None], loop=True, length_beats=8.0))
    bass.gain = 0.7

    # Harp arpeggios
    harp = song.create_track("Harp", Harp())
    c_major = Scale("C", "major")
    harp_notes = [str(n) for n in c_major.get_notes(octave=4)]
    harp.set_pattern(Pattern(harp_notes, loop=True, length_beats=4.0))
    harp.gain = 0.4

    # Woodwinds
    flute = song.create_track("Flute", Flute())
    flute.set_pattern(Pattern(["G5", "A5", "B5", "G5"], loop=True, length_beats=8.0))
    flute.gain = 0.4

    oboe = song.create_track("Oboe", Oboe())
    oboe.set_pattern(Pattern(["E5", None, "D5", "C5"], loop=True, length_beats=8.0))
    oboe.gain = 0.35

    bassoon = song.create_track("Bassoon", Bassoon())
    bassoon.set_pattern(Pattern(["C3", None, "F2", None], loop=True, length_beats=8.0))
    bassoon.gain = 0.45

    # Brass
    horn = song.create_track("FrenchHorn", FrenchHorn())
    horn.set_pattern(Pattern(["C4", None, "E4", None], loop=True, length_beats=8.0))
    horn.gain = 0.4

    trumpet = song.create_track("Trumpet", Trumpet())
    trumpet.set_pattern(Pattern([None, None, "G4", "E4"], loop=True, length_beats=8.0))
    trumpet.gain = 0.3

    # Percussion
    timpani = song.create_track("Timpani", Timpani())
    timpani.set_pattern(Pattern(["C2", None, None, None, "G1", None, None, None], loop=True, length_beats=8.0))
    timpani.gain = 0.6

    gong = song.create_track("Gong", Gong())
    gong.set_pattern(Pattern(["C2"], loop=False))
    gong.gain = 0.3

    print("Rendering orchestral_demo.wav...")
    song.render("orchestral_demo.wav")
    print("Done!")


if __name__ == "__main__":
    main()

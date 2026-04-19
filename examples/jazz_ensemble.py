from pymusik.composition.pattern import Pattern
from pymusik.instruments.keys import Rhodes, Clavinet
from pymusik.instruments.bass import UprightBass, FretlessBass
from pymusik.instruments.brass import Trumpet, Trombone
from pymusik.instruments.woodwinds import SaxInstrument
from pymusik.instruments.choir import VocalOoh
from pymusik.instruments.drums import DrumInstrument
from pymusik.engine.audio_graph import Song


def main():
    print("=== Jazz Ensemble Demo ===")

    song = Song(name="Late Night Jazz", bpm=95)

    # Upright bass walking line
    bass = song.create_track("UprightBass", UprightBass())
    bass.set_pattern(Pattern(["C2", "E2", "G2", "A2", "D2", "F2", "A2", "B2"], loop=True, length_beats=8.0))
    bass.gain = 0.65

    # Rhodes chords
    rhodes = song.create_track("Rhodes", Rhodes())
    rhodes.set_pattern(Pattern(["C4", "E4", "G4", "B4", "D4", "F4", "A4", "C5"], loop=True, length_beats=8.0))
    rhodes.gain = 0.4

    # Clavinet comping
    clav = song.create_track("Clavinet", Clavinet())
    clav.set_pattern(Pattern(["Eb4", None, "G4", None, "F4", None, "D4", None], loop=True, length_beats=8.0))
    clav.gain = 0.35

    # Trumpet melody
    trumpet = song.create_track("Trumpet", Trumpet())
    trumpet.set_pattern(Pattern(["G5", None, "E5", "D5", "C5", None, None, "E5"], loop=True, length_beats=8.0))
    trumpet.gain = 0.4

    # Trombone
    trombone = song.create_track("Trombone", Trombone())
    trombone.set_pattern(Pattern(["C3", None, None, "G3", None, None, "E3", None], loop=True, length_beats=8.0))
    trombone.gain = 0.35

    # Sax (from lofi module)
    from pymusik.instruments.lofi import SaxInstrument
    sax = song.create_track("Sax", SaxInstrument())
    sax.set_pattern(Pattern([None, "A4", None, "G4", "F4", None, "E4", None], loop=True, length_beats=8.0))
    sax.gain = 0.4

    # Brush drums
    drums = song.create_track("Drums", DrumInstrument())
    drums.set_pattern(Pattern(["C1", "F#1", "D1", "F#1", "C1", "F#1", "D1", "F#1"], loop=True, length_beats=8.0))
    drums.gain = 0.45

    # Vocal pad
    vocal = song.create_track("VocalPad", VocalOoh())
    vocal.set_pattern(Pattern(["C4", "Eb4", "G4", "Bb4"], loop=True, length_beats=8.0))
    vocal.gain = 0.2

    print("Rendering jazz_ensemble.wav...")
    song.render("jazz_ensemble.wav")
    print("Done!")


if __name__ == "__main__":
    main()

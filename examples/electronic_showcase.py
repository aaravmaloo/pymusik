from pymusik.composition.pattern import Pattern
from pymusik.instruments.electronic import TB303, SupersawPad, WavetableLead, FMBass, TranceGate, ChiptuneLead, ChiptuneBass
from pymusik.instruments.bass import WobbleBass, SubBass
from pymusik.instruments.pro import ProDrums
from pymusik.engine.audio_graph import Song


def main():
    print("=== Electronic Showcase ===")

    song = Song(name="Synth Odyssey", bpm=128)

    # Pro drums
    drums = song.create_track("Drums", ProDrums())
    drum_pat = Pattern(["C1", "F1", "C1", "F1", "D1", "F1", "C1", "F1"], loop=True, length_beats=8.0)
    drums.set_pattern(drum_pat)
    drums.gain = 0.7

    # TB-303 acid line
    tb = song.create_track("TB303", TB303())
    tb.set_pattern(Pattern(["C3", "Eb3", "G3", "C3", "Bb2", "G2", "C3", None], loop=True, length_beats=8.0))
    tb.gain = 0.5
    tb.sidechain = True

    # FM Bass
    fm = song.create_track("FMBass", FMBass())
    fm.set_pattern(Pattern(["C2", "C2", "G1", "C2"], loop=True, length_beats=4.0))
    fm.gain = 0.6
    fm.sidechain = True

    # Wobble bass
    wobble = song.create_track("WobbleBass", WobbleBass())
    wobble.set_pattern(Pattern(["C1", None, "C1", None], loop=True, length_beats=4.0))
    wobble.gain = 0.5
    wobble.sidechain = True

    # Supersaw pad
    pad = song.create_track("SupersawPad", SupersawPad())
    pad.set_pattern(Pattern(["C4", "Eb4", "G4", "Bb4"], loop=True, length_beats=8.0))
    pad.gain = 0.3

    # Wavetable lead
    lead = song.create_track("WavetableLead", WavetableLead())
    lead.set_pattern(Pattern(["G4", "Bb4", "C5", "Eb5", "G5", "Eb5", "C5", "Bb4"], loop=True, length_beats=8.0))
    lead.gain = 0.4

    # Trance gate
    gate = song.create_track("TranceGate", TranceGate())
    gate.set_pattern(Pattern(["C5", "Eb5", "G5", "Bb5"], loop=True, length_beats=4.0))
    gate.gain = 0.3

    # Chiptune section
    chip_lead = song.create_track("ChiptuneLead", ChiptuneLead())
    chip_lead.set_pattern(Pattern(["C5", "E5", "G5", "C6", "G5", "E5", "C5", None], loop=True, length_beats=8.0))
    chip_lead.gain = 0.25

    chip_bass = song.create_track("ChiptuneBass", ChiptuneBass())
    chip_bass.set_pattern(Pattern(["C2", "C2", "G1", "G1"], loop=True, length_beats=4.0))
    chip_bass.gain = 0.35

    print("Rendering electronic_showcase.wav...")
    song.render("electronic_showcase.wav")
    print("Done!")


if __name__ == "__main__":
    main()
